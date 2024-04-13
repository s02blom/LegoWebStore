# Lego Web Store

## Description
This project models the data necessary for runing a manutacturing/ distribution center for lego. The project is a part of the course work for DV 1663 VT24.

## python-sql-devcontainer
This repository contains a dev container with a MySQL server and python. It also installs the necessary VS Code extentions to confortably run and develop the repository along with the python libraries to run all the code. 

### Env-file
The `.env` file should be located inside [`.devcontainer`](./.devcontainer/). Here is an example of an appripriate `.env` file:
```
DATABASE_HOST=mysql_db
DATABASE_USER=ROOT
DATABASE_PASSWORD=my-password
DATABASE_DB=my-database
DATABASE_PORT=3306
```
Do note however that this is the default port for MySQL Workbench and you might wish to change the port if you plan using that at the same time. 

## Figures
All figures are a UML diagrams written using (PlantUML)[https://plantuml.com/]. 

## License

AUTHORS:
 - [Ninni Salomonsson](https://github.com/NinniS)
 - [Sofia Blom](https://github.com/s02blom)
 
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file details