WITH base AS (
    SELECT
        "CLINIC ID" AS clinic_id,
        "VISIT MONTH YEAR" AS visit_month,
        "TOTAL OMNI SALES ($)" AS sales,
        "TOTAL OMNI SALES (LBS)" AS volume,
        "TOTAL EDUCATION COST ($)" AS edu_cost,
        CASE
            WHEN "COUNT OF PCV-ONLY EDUCATIONS" > 0
              OR "COUNT OF PCV-TM (PCV ORGANIZED) EDUCATIONS" > 0
              OR "COUNT OF PCV-TM (PCV OWNED) EDUCATIONS" > 0          THEN 'PCV INVOLVED'
            WHEN "COUNT OF NO-PCV-INVOLVED EDUCATIONS" > 0             THEN 'NO PCV INVOLVED'
            ELSE 'NO EDUCATION'
        END AS pcv_type,
        MIN(CASE WHEN "COUNT OF PCV-ONLY EDUCATIONS" > 0
                   OR "COUNT OF PCV-TM (PCV ORGANIZED) EDUCATIONS" > 0
                   OR "COUNT OF PCV-TM (PCV OWNED) EDUCATIONS" > 0
                   OR "COUNT OF NO-PCV-INVOLVED EDUCATIONS" > 0
                 THEN "VISIT MONTH YEAR" END)
            OVER (PARTITION BY "CLINIC ID") AS first_edu_month
    FROM dev_ext_sales_hub.hills_us.con_hills_us_clinic_dna_pcv_educations_monthly_sales
),

windowed AS (
    SELECT
        *,
        DATEDIFF('month', visit_month, first_edu_month) AS months_before_edu,
        DATEDIFF('month', first_edu_month, visit_month) AS months_after_edu,

        -- Window flags 
        CASE WHEN DATEDIFF('month', visit_month,    first_edu_month) BETWEEN 1  AND 6  THEN 1 ELSE 0 END AS cy_pre_6m,
        CASE WHEN DATEDIFF('month', first_edu_month, visit_month)    BETWEEN 0  AND 5  THEN 1 ELSE 0 END AS cy_post_6m,
        CASE WHEN DATEDIFF('month', visit_month,    first_edu_month) BETWEEN 1  AND 12 THEN 1 ELSE 0 END AS cy_pre_12m,
        CASE WHEN DATEDIFF('month', first_edu_month, visit_month)    BETWEEN 0  AND 11 THEN 1 ELSE 0 END AS cy_post_12m,
        CASE WHEN DATEDIFF('month', visit_month,    first_edu_month) BETWEEN 13 AND 18 THEN 1 ELSE 0 END AS ly_pre_6m,
        CASE WHEN DATEDIFF('month', visit_month,    first_edu_month) BETWEEN 7  AND 12 THEN 1 ELSE 0 END AS ly_post_6m,
        CASE WHEN DATEDIFF('month', visit_month,    first_edu_month) BETWEEN 13 AND 24 THEN 1 ELSE 0 END AS ly_pre_12m,
        CASE WHEN DATEDIFF('month', visit_month,    first_edu_month) BETWEEN 7  AND 12 THEN 1 ELSE 0 END AS baseline_trend_6m,

        -- Window label 
        CASE
            WHEN DATEDIFF('month', visit_month, first_edu_month) > 24
                THEN 'BEFORE WINDOW (mo -' || DATEDIFF('month', visit_month, first_edu_month)::VARCHAR || ')'
            WHEN DATEDIFF('month', visit_month, first_edu_month) BETWEEN 13 AND 24
                THEN 'LY PRE-12M (mo -' || DATEDIFF('month', visit_month, first_edu_month)::VARCHAR || ')'
            WHEN DATEDIFF('month', visit_month, first_edu_month) BETWEEN 7 AND 12
                THEN 'LY POST-6M / BASELINE (mo -' || DATEDIFF('month', visit_month, first_edu_month)::VARCHAR || ')'
            WHEN DATEDIFF('month', visit_month, first_edu_month) BETWEEN 1 AND 6
                THEN 'CY PRE-6M (mo -' || DATEDIFF('month', visit_month, first_edu_month)::VARCHAR || ')'
            WHEN DATEDIFF('month', first_edu_month, visit_month) = 0
                THEN 'EDUCATION MONTH (mo 0)'
            WHEN DATEDIFF('month', first_edu_month, visit_month) BETWEEN 1 AND 5
                THEN 'CY POST-6M (mo +' || DATEDIFF('month', first_edu_month, visit_month)::VARCHAR || ')'
            WHEN DATEDIFF('month', first_edu_month, visit_month) BETWEEN 6 AND 11
                THEN 'CY POST-12M (mo +' || DATEDIFF('month', first_edu_month, visit_month)::VARCHAR || ')'
            WHEN DATEDIFF('month', first_edu_month, visit_month) >= 12
                THEN 'BEYOND 12M (mo +' || DATEDIFF('month', first_edu_month, visit_month)::VARCHAR || ')'
        END AS window_label,

        -- Volatility metrics (clinic-level, repeated on every row)
        MAX(sales)  OVER (PARTITION BY clinic_id) AS clinic_max_monthly_sales,
        AVG(sales)  OVER (PARTITION BY clinic_id) AS clinic_avg_monthly_sales,
        MAX(sales)  OVER (PARTITION BY clinic_id)
            / NULLIF(AVG(sales) OVER (PARTITION BY clinic_id), 0) AS peak_to_avg_ratio

    FROM base
),

-- Monthly detail: one row per clinic x month
monthly_detail AS (
    SELECT
        clinic_id,
        visit_month,
        first_edu_month,
        pcv_type,
        window_label,
        months_before_edu,
        months_after_edu,
        ROUND(SUM(sales),   2) AS monthly_sales,
        ROUND(SUM(volume),  2) AS monthly_volume,
        ROUND(SUM(edu_cost),2) AS monthly_edu_cost,
        ROUND(MAX(peak_to_avg_ratio), 1) AS peak_to_avg_ratio,
        CASE
            WHEN MAX(peak_to_avg_ratio) >= 5 THEN 'HIGH VOLATILITY'
            WHEN MAX(peak_to_avg_ratio) >= 2 THEN 'MODERATE VOLATILITY'
            ELSE 'STABLE'
        END AS volatility_flag,

        -- Month-over-month change
        ROUND(SUM(sales) - LAG(SUM(sales)) OVER (
            PARTITION BY clinic_id ORDER BY visit_month
        ), 2) AS mom_change,

        -- Same month last year
        ROUND(LAG(SUM(sales), 12) OVER (
            PARTITION BY clinic_id ORDER BY visit_month
        ), 2) AS same_month_ly_sales,

        -- YoY change
        ROUND(SUM(sales) - LAG(SUM(sales), 12) OVER (
            PARTITION BY clinic_id ORDER BY visit_month
        ), 2) AS yoy_change,

        -- Cumulative sales
        ROUND(SUM(SUM(sales)) OVER (
            PARTITION BY clinic_id
            ORDER BY visit_month
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ), 2) AS cumulative_sales

    FROM windowed
    GROUP BY clinic_id, visit_month, first_edu_month, pcv_type,
             window_label, months_before_edu, months_after_edu
),

-- Window aggregates: one row per clinic x pcv_type─
clinic_agg AS (
    SELECT
        clinic_id,
        pcv_type,
        first_edu_month,
        SUM(edu_cost) AS total_edu_cost,
        COUNT(DISTINCT visit_month) AS total_months_of_data,
        ROUND(MAX(peak_to_avg_ratio), 1) AS peak_to_avg_ratio,
        CASE
            WHEN MAX(peak_to_avg_ratio) >= 5 THEN 'HIGH VOLATILITY'
            WHEN MAX(peak_to_avg_ratio) >= 2 THEN 'MODERATE VOLATILITY'
            ELSE 'STABLE'
        END AS volatility_flag,

        SUM(CASE WHEN cy_pre_6m         = 1 THEN sales ELSE 0 END) AS cy_sales_6m_before_edu,
        SUM(CASE WHEN cy_post_6m        = 1 THEN sales ELSE 0 END) AS cy_sales_6m_after_edu,
        SUM(CASE WHEN cy_pre_12m        = 1 THEN sales ELSE 0 END) AS cy_sales_12m_before_edu,
        SUM(CASE WHEN cy_post_12m       = 1 THEN sales ELSE 0 END) AS cy_sales_12m_after_edu,
        SUM(CASE WHEN ly_pre_6m         = 1 THEN sales ELSE 0 END) AS ly_sales_same_6m_pre_window,
        SUM(CASE WHEN ly_post_6m        = 1 THEN sales ELSE 0 END) AS ly_sales_same_6m_post_window,
        SUM(CASE WHEN ly_pre_12m        = 1 THEN sales ELSE 0 END) AS ly_sales_12m_benchmark,
        SUM(CASE WHEN baseline_trend_6m = 1 THEN sales ELSE 0 END) AS sales_6m_to_12m_before_edu,
        SUM(CASE WHEN cy_pre_6m         = 1 THEN volume ELSE 0 END) AS cy_volume_6m_before_edu,
        SUM(CASE WHEN cy_post_6m        = 1 THEN volume ELSE 0 END) AS cy_volume_6m_after_edu,
        SUM(CASE WHEN cy_pre_12m        = 1 THEN volume ELSE 0 END) AS cy_volume_12m_before_edu,
        SUM(CASE WHEN cy_post_12m       = 1 THEN volume ELSE 0 END) AS cy_volume_12m_after_edu

    FROM windowed
    GROUP BY clinic_id, pcv_type, first_edu_month
),

-- Window summary: all derived metrics
window_summary AS (
    SELECT
        clinic_id,
        pcv_type,
        first_edu_month,
        total_edu_cost,
        total_months_of_data,
        peak_to_avg_ratio,
        volatility_flag,

        -- Raw before/after 6m
        ROUND(cy_sales_6m_before_edu, 2) AS cy_sales_6m_before_edu,
        ROUND(cy_sales_6m_after_edu,  2) AS cy_sales_6m_after_edu,
        ROUND(cy_sales_6m_after_edu - cy_sales_6m_before_edu, 2) AS raw_uplift_6m,
        ROUND((cy_sales_6m_after_edu - cy_sales_6m_before_edu)
            / NULLIF(cy_sales_6m_before_edu, 0) * 100, 1) AS raw_uplift_pct_6m,

        -- Raw before/after 12m
        ROUND(cy_sales_12m_before_edu, 2) AS cy_sales_12m_before_edu,
        ROUND(cy_sales_12m_after_edu,  2) AS cy_sales_12m_after_edu,
        ROUND(cy_sales_12m_after_edu - cy_sales_12m_before_edu, 2) AS raw_uplift_12m,
        ROUND((cy_sales_12m_after_edu - cy_sales_12m_before_edu)
            / NULLIF(cy_sales_12m_before_edu, 0) * 100, 1) AS raw_uplift_pct_12m,

        -- LY 6m control
        ROUND(ly_sales_same_6m_pre_window,  2) AS ly_sales_same_6m_pre_window,
        ROUND(ly_sales_same_6m_post_window, 2) AS ly_sales_same_6m_post_window,
        ROUND(ly_sales_same_6m_post_window - ly_sales_same_6m_pre_window, 2) AS ly_natural_swing_6m,
        ROUND((ly_sales_same_6m_post_window - ly_sales_same_6m_pre_window)
            / NULLIF(ly_sales_same_6m_pre_window, 0) * 100, 1) AS ly_natural_swing_pct_6m,

        -- LY 12m benchmark
        ROUND(ly_sales_12m_benchmark, 2) AS ly_sales_12m_benchmark,
        ROUND(cy_sales_12m_after_edu - ly_sales_12m_benchmark, 2) AS cy_post_vs_ly_benchmark_12m,
        ROUND((cy_sales_12m_after_edu - ly_sales_12m_benchmark)
            / NULLIF(ly_sales_12m_benchmark, 0) * 100, 1) AS cy_post_vs_ly_benchmark_pct_12m,

        -- Incremental uplift (education effect net of natural trend)
        ROUND((cy_sales_6m_after_edu   - cy_sales_6m_before_edu)
            - (ly_sales_same_6m_post_window - ly_sales_same_6m_pre_window), 2) AS edu_incremental_uplift_6m,

        -- Pre-education trajectory
        ROUND(sales_6m_to_12m_before_edu, 2) AS sales_6m_to_12m_before_edu,
        ROUND((cy_sales_6m_before_edu - sales_6m_to_12m_before_edu)
            / NULLIF(sales_6m_to_12m_before_edu, 0) * 100, 1) AS pre_edu_trajectory_pct,

        -- True ROI 6m (incremental uplift minus education cost)
        ROUND((cy_sales_6m_after_edu   - cy_sales_6m_before_edu)
            - (ly_sales_same_6m_post_window - ly_sales_same_6m_pre_window)
            - total_edu_cost, 2) AS true_net_roi_6m,
        ROUND(((cy_sales_6m_after_edu  - cy_sales_6m_before_edu)
            - (ly_sales_same_6m_post_window - ly_sales_same_6m_pre_window)
            - total_edu_cost)
            / NULLIF(total_edu_cost, 0) * 100, 1) AS true_roi_pct_6m,

        -- Volume uplift
        ROUND(cy_volume_6m_after_edu  - cy_volume_6m_before_edu,  2) AS volume_uplift_6m,
        ROUND(cy_volume_12m_after_edu - cy_volume_12m_before_edu, 2) AS volume_uplift_12m

    FROM clinic_agg
)

-- Final output: monthly rows with window summary joined─
SELECT
    -- Identity & context
    m.clinic_id,
    m.visit_month,
    m.first_edu_month,
    m.window_label,
    m.months_before_edu,
    m.months_after_edu,
    m.pcv_type,

    -- Monthly detail
    m.monthly_sales,
    m.monthly_volume,
    m.monthly_edu_cost,
    m.mom_change,
    m.same_month_ly_sales,
    m.yoy_change,
    m.volatility_flag,
    m.peak_to_avg_ratio,
    m.cumulative_sales,

    -- Window summary
    w.total_edu_cost,
    w.total_months_of_data,

    -- Raw before/after
    w.cy_sales_6m_before_edu,
    w.cy_sales_6m_after_edu,
    w.raw_uplift_6m,
    w.raw_uplift_pct_6m,
    w.cy_sales_12m_before_edu,
    w.cy_sales_12m_after_edu,
    w.raw_uplift_12m,
    w.raw_uplift_pct_12m,

    -- LY control
    w.ly_sales_same_6m_pre_window,
    w.ly_sales_same_6m_post_window,
    w.ly_natural_swing_6m,
    w.ly_natural_swing_pct_6m,
    w.ly_sales_12m_benchmark,
    w.cy_post_vs_ly_benchmark_12m,
    w.cy_post_vs_ly_benchmark_pct_12m,

    -- Incremental uplift & trajectory
    w.edu_incremental_uplift_6m,
    w.sales_6m_to_12m_before_edu,
    w.pre_edu_trajectory_pct,

    -- True ROI
    w.true_net_roi_6m,
    w.true_roi_pct_6m,

    -- Volume
    w.volume_uplift_6m,
    w.volume_uplift_12m

FROM monthly_detail m
LEFT JOIN window_summary w
    ON  m.clinic_id       = w.clinic_id
    AND m.pcv_type        = w.pcv_type
    AND m.first_edu_month = w.first_edu_month
where m.clinic_id = '764869'
ORDER BY m.clinic_id, m.visit_month;
