SHOW DATABASES;
USE retail_db;
SHOW TABLES;
select * from credit_risk_clean; 
# Count Row
SELECT COUNT(*) 
FROM credit_risk_clean; 

-- Q1. What percentage of the total loans does each loan status represent?
SELECT 
    loan_status,
    COUNT(*) AS total_loans,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 
        2
    ) AS percentage
FROM credit_risk_clean
GROUP BY loan_status
ORDER BY total_loans DESC;

-- Q2. What is the ratio of 'bad' loans (Charged Off / Default) compared to 'good' loans?
SELECT
    CASE 
        WHEN loan_status = 'Charged Off' THEN 'Bad Loan'
        ELSE 'Good Loan'
    END AS loan_type,
    COUNT(*) AS total
FROM credit_risk_clean
GROUP BY loan_type;

#####
-- Q3. What is the most common type of home ownership among the borrowers?
SELECT 
    person_home_ownership,
    COUNT(*) AS total_customers
FROM credit_risk_clean
GROUP BY person_home_ownership
ORDER BY total_customers DESC;

-- Q4. Which loan purpose appears most frequently in the dataset?
SELECT 
    loan_intent,
    COUNT(*) AS total_loans
FROM credit_risk_clean
GROUP BY loan_intent
ORDER BY total_loans DESC;

-- Q5. How are loan grades distributed?
SELECT 
    loan_grade,
    COUNT(*) AS total_loans
FROM credit_risk_clean
GROUP BY loan_grade
ORDER BY loan_grade;

-- Q6. How many of these customers have a history of default in the past?
SELECT 
    cb_person_default_on_file,
    COUNT(*) AS total_customers
FROM credit_risk_clean
GROUP BY cb_person_default_on_file;

-- Q7.Do default rates differ across different categories?
SELECT 
    person_home_ownership,
    loan_status,
    COUNT(*) AS total_loans
FROM credit_risk_clean
GROUP BY person_home_ownership, loan_status
ORDER BY person_home_ownership, total_loans DESC;

-- Q8. Does loan grade moderate the relationship between loan amount and default risk?
WITH RankedLoans AS (
    SELECT 
        loan_status, 
        loan_grade, 
        loan_amnt,
        ROW_NUMBER() OVER (PARTITION BY loan_status, loan_grade ORDER BY loan_amnt) as row_num,
        COUNT(*) OVER (PARTITION BY loan_status, loan_grade) as total_count
    FROM credit_risk_clean
)
SELECT 
    loan_status, 
    loan_grade,
    total_count AS total_loans,
    AVG(loan_amnt) AS avg_loan_amount,
    AVG(CASE WHEN row_num IN (FLOOR((total_count+1)/2), CEIL((total_count+1)/2)) 
             THEN loan_amnt END) AS median_loan_amount
FROM RankedLoans
GROUP BY loan_status, loan_grade, total_count
ORDER BY loan_status, loan_grade;












