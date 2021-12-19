## To run this program and test if it works

```
 -- we need to start up the virtual machine first. For this go to the vagrant directory.
 -- once inside, type the command vagrant up.
 -- the VM will start booting. Once this is done, type vagrant ssh.
 -- After this is done , you need to go to  the directory cd /vagrant/tournament (cd means change directory)
 -- before testing, we need to setup the database.
 -- to do this we need to import the create database and create table statements from the tournament.sql file
 -- type the command psql -f tournament.sql
 -- the database and then all the tables will be created and the table constraints will be setup.
 -- we need to exit psql by pressing ctrl + D key.
 -- once this is done, we need to run command python tournament_test.py to check if all our unit tests pass.
 ```
