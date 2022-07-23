If you want to generate the schema,


## From dot file to png
1. Install django-extension with graphviz in virtual environment
2. ```python manage.py graph_models -a > my_project.dot``` will create a dot file capturing all schemas (the project has been configured, if not refer to official docs for customization)
2. ```dot -Tpng generated.dot -o generated.png``` convert to png. You will need ```graphviz`` (This step can be run outside or inside of virtual environment. Just ensure graphiz is installed.




