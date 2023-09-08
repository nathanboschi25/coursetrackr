SELECT DISTINCT DATE(start_datetime) AS date
FROM signature_list sl
         JOIN events ev ON sl.list_id = ev.list_id
WHERE sl.list_id = 1
  AND ev.start_datetime >= '2023-09-04'
  AND ev.end_datetime <= '2023-09-10'
ORDER BY start_datetime;

SELECT *
FROM events ev
         LEFT JOIN signatures s ON ev.event_id = s.event_id
WHERE DATE(start_datetime) = '2023-09-04'
ORDER BY start_datetime;

SELECT ev.*,
       s.*,
       t.teacher_name
FROM events ev
         LEFT JOIN signatures s ON ev.event_id = s.event_id
         LEFT JOIN teachers t ON t.teacher_id = s.teacher_id
WHERE DATE(start_datetime) = '2023-09-04'
  AND ev.list_id = 1
ORDER BY start_datetime;