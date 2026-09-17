-- Quelles villes auront les températures les plus élevées ?

SELECT c.name , MAX(w.temp_max) as top_temp FROM cities c
JOIN weather_risks w on w.city_id = c.id
GROUP BY c.name 
ORDER BY top_temp DESC LIMIT 5;   

-- Quelles villes auront les plus fortes précipitations ?
SELECT c.name , MAX(w.precip_max) as top_precipitation FROM cities c
JOIN weather_risks w on w.city_id = c.id
GROUP BY c.name 
ORDER BY top_precipitation DESC LIMIT 5;

-- Quelles villes présentent le risque moyen le plus élevé ?
SELECT c.name , AVG(w.risk_total) as top_risk FROM cities c
JOIN weather_risks w on w.city_id = c.id
GROUP BY c.name 
ORDER BY top_risk DESC LIMIT 5;

-- Quelles périodes présentent le risque maximal ?

SELECT date , risk_total FROM weather_risks
WHERE risk_total = (SELECT MAX(risk_total) from weather_risks);

-- nombre de villes ;
SELECT COUNT(id) FROM cities;
-- température maximale ;
SELECT MAX(temp_max) from weather_risks;
-- précipitations maximales ;
SELECT MAX(precip_max) from weather_risks;