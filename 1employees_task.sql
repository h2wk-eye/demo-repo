CREATE TABLE departments (
    department_id INT NOT NULL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

CREATE TABLE positions (
    position_id INT NOT NULL PRIMARY KEY,
    position_name VARCHAR(100) NOT NULL
);

CREATE TABLE projects (
    project_id INT NOT NULL PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE TABLE employees (
    employee_id INT NOT NULL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    department_id INT REFERENCES departments(department_id),
    position_id INT REFERENCES positions(position_id),
    date_on_position DATE NOT NULL,
    date_in_department DATE NOT NULL,
    salary DECIMAL(10, 2) NOT NULL
);

CREATE TABLE employee_projects (
    project_id INT NOT NULL REFERENCES projects(project_id),
	employee_id INT NOT NULL REFERENCES employees(employee_id)
);

INSERT INTO departments (department_id, department_name)
VALUES
    (1,'Снабжение'),
    (2,'Разработка'),
    (3,'Логистика');

INSERT INTO positions(position_id, position_name)
VALUES
    (1,'Менеджер'),
    (2,'Дизайнер'),
    (3,'Разработчик');

INSERT INTO employees (employee_id, full_name, department_id, position_id, date_on_position, date_in_department, salary)
VALUES
    (1,'Иван Петров', 1, 2, '2020-01-15', '2020-01-15', 600000),
    (2,'Петр Петров', 2, 2, '2019-05-20', '2020-01-15', 500000),
    (3,'Сидр Сидоров ', 2, 3, '2018-08-10', '2021-01-15', 300000),
    (4,'Марчук Ольга', 3, 2, '2021-03-02', '2021-01-15', 450000),
	(5,'Давид Скворцов', 3, 2, '2020-05-15', '2022-01-15', 420000),
    (6,'Петр Синичкин', 1, 3, '2019-09-20', '2021-01-15', 300000),
    (7,'Сидр Егоров', 2, 1, '2018-01-10', '2021-01-15', 120000),
    (8,'Ольга Николаева', 2, 2, '2021-01-02', '2022-01-15', 420000),
    (9,'Давид Кузнецов', 1, 1, '2020-01-11', '2022-01-15', 550000),
    (10,'Петр Москвин', 1, 3, '2019-05-12', '2022-01-15', 400000),
    (11,'Сидр Величко', 3, 3, '2018-08-13', '2021-01-15', 720000),
    (12,'Ольга Морозова ', 3, 1, '2021-03-22', '2020-01-15', 410000);
  
INSERT INTO projects(project_id, project_name, start_date, end_date)
VALUES
    (1,'App development', '2020-01-02', '2023-01-02'),
    (2,'App testing', '2021-01-02', '2022-01-02'),
    (3,'Parsing', '2021-01-02', '2021-11-02'),
    (4,'Website', '2022-01-02', '2022-05-12');

INSERT INTO employee_projects(project_id, employee_id)
VALUES
    (1, 3),
	(1, 12),
    (1, 4),
    (2, 5),
    (2, 3), 
    (3, 1),
    (3, 4),
    (4, 1),
    (4, 2),
    (4, 6),
    (4, 12);

--1--
select e.full_name, e.salary, p.position_name from employees e
join positions p on e.position_id = p.position_id
where e.full_name like 'Давид %';

--2--
select d.department_name, avg(e.salary) as avg_salary from employees e
join departments d on d.department_id = e.department_id
group by d.department_name;

--3--
select q1.*, CASE
    when avg_salary > (select avg(salary) from employees) THEN 'Yes'
    else 'No'
	end as is_bigger_than_avg_salary 
from (
select p.position_name, avg(e.salary) as avg_salary from employees e
join positions p on e.position_id = p.position_id
group by p.position_id
) q1; 

--4--
CREATE VIEW position_summary AS
SELECT p.position_name,
    ARRAY_AGG(DISTINCT d.department_name) AS departments,
    AVG(e.salary) AS "Средняя ЗП"
FROM positions p
LEFT JOIN employees e ON p.position_id = e.position_id
LEFT JOIN departments d ON e.department_id = d.department_id
GROUP BY p.position_name;

SELECT * FROM position_summary
