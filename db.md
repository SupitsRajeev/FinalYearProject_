<!-- Get user list for super user -->
<!-- 
select *
from user where isHr = 1 and isIt = 1
-->

## Get user list for Hr user
<!- 
select *
from user where isHr = 1 and isIt = 0
  -->

## Get user list for IT user
<!-- 
select *
from user where isHr = 0 and isIt = 1
-->


## insert the following seed data while generating the application.use migration script. replace the 123 field of password
## with generated
<!--INSERT INTO pamdb.user (id, name, email, password, isHr, isIt, created_date, created_by, updated_by, updated_date) VALUES (1, 'Davit', 'davitkhanal@gmai.com', '123', 1, 1, null, 'rajev', 'rajev', null);
INSERT INTO pamdb.user (id, name, email, password, isHr, isIt, created_date, created_by, updated_by, updated_date) VALUES (2, 'Rajeev', 'rajeev@gmai.com', '123', 1, 1, null, 'davit', 'davit', null);
INSERT INTO pamdb.user (id, name, email, password, isHr, isIt, created_date, created_by, updated_by, updated_date) VALUES (3, 'Subin', 'subin@gmai.com', '123', 1, 0, null, 'davit', 'davit', null);
INSERT INTO pamdb.user (id, name, email, password, isHr, isIt, created_date, created_by, updated_by, updated_date) VALUES (4, 'prekshya', 'prekshya@gmai.com', '123', 1, 0, null, 'davit', 'davit', null);
 >

<!-- Add into user priviledgeGroups -->
 <!-- INSERT INTO pamdb.user_priviledge_groups (Id, name, role_level, created_date, created_by, updated_date, updated_by) VALUES (1, 'Superuser', 1, null, null, null, null);
INSERT INTO pamdb.user_priviledge_groups (Id, name, role_level, created_date, created_by, updated_date, updated_by) VALUES (2, 'Priviledgeuser', 2, null, null, null, null);
INSERT INTO pamdb.user_priviledge_groups (Id, name, role_level, created_date, created_by, updated_date, updated_by) VALUES (3, 'Normaluser', 3, null, null, null, null); -->



<!-- INSERT INTO pamdb.user_priviledge (id, userId, priviledge_groups_role, created_by, created_at, updated_by, updated_at) VALUES (1, 1, 1, null, null, null, null);
INSERT INTO pamdb.user_priviledge (id, userId, priviledge_groups_role, created_by, created_at, updated_by, updated_at) VALUES (2, 2, 1, null, null, null, null);
INSERT INTO pamdb.user_priviledge (id, userId, priviledge_groups_role, created_by, created_at, updated_by, updated_at) VALUES (3, 3, 2, null, null, null, null);
INSERT INTO pamdb.user_priviledge (id, userId, priviledge_groups_role, created_by, created_at, updated_by, updated_at) VALUES (4, 4, 3, null, null, null, null); -->



<!-- To Check the priviledge level of any user -->

<!-- select u.name,upg.name from user_priviledge up
    inner join user_priviledge_groups upg on up.priviledge_groups_role = upg.role_level
inner join user u on up.userId = u.id -->