SELECT user_id,
       SUM(reward) AS total_reward_2022
FROM reports
WHERE user_id IN (
    SELECT user_id
    FROM reports
    WHERE EXTRACT(YEAR FROM created_at) = 2021
    GROUP BY user_id
    HAVING MIN(created_at) BETWEEN '2021-01-01' AND '2021-12-31'
)
AND EXTRACT(YEAR FROM created_at) = 2022
GROUP BY user_id;