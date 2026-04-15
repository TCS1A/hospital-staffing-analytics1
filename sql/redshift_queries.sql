-- METRIC 1: Nurse-to-Patient Ratio by State
SELECT
    STATE,
    ROUND(AVG((Hrs_RN + Hrs_LPN + Hrs_CNA) / NULLIF(MDScensus, 0)), 2) AS avg_nurse_patient_ratio
FROM staffing_staging
GROUP BY STATE
ORDER BY avg_nurse_patient_ratio DESC;

-- METRIC 2: Total Nursing Hours by State
SELECT
    STATE,
    ROUND(SUM(Hrs_RN), 0)                      AS total_rn_hours,
    ROUND(SUM(Hrs_LPN), 0)                     AS total_lpn_hours,
    ROUND(SUM(Hrs_CNA), 0)                     AS total_cna_hours,
    ROUND(SUM(Hrs_RN + Hrs_LPN + Hrs_CNA), 0) AS total_nurse_hours
FROM staffing_staging
GROUP BY STATE
ORDER BY total_nurse_hours DESC;

-- METRIC 3: Employee vs Contract Hours
SELECT
    ROUND(SUM(Hrs_RN_emp + Hrs_LPN_emp + Hrs_CNA_emp), 0) AS employee_hours,
    ROUND(SUM(Hrs_RN_ctr + Hrs_LPN_ctr + Hrs_CNA_ctr), 0) AS contract_hours
FROM staffing_staging;

-- METRIC 4: Most Understaffed Facilities
SELECT
    PROVNUM, PROVNAME, STATE,
    ROUND(AVG(MDScensus), 1) AS avg_patients,
    ROUND(AVG((Hrs_RN + Hrs_LPN + Hrs_CNA) / NULLIF(MDScensus,0)), 2) AS nurse_patient_ratio
FROM staffing_staging
GROUP BY PROVNUM, PROVNAME, STATE
ORDER BY nurse_patient_ratio ASC
LIMIT 20;

-- METRIC 5: Patient Census Trend
SELECT
    DATE_TRUNC('month', CAST(WorkDate AS DATE)) AS month,
    ROUND(AVG(MDScensus), 1) AS avg_patients,
    COUNT(DISTINCT PROVNUM)  AS total_facilities
FROM staffing_staging
GROUP BY 1
ORDER BY 1;
