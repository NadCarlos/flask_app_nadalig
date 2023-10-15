## Docker y docker-compose

####Para los que estaban teniendo problemas con la db.

Con este comando van a borrar los volúmenes asociados al docker-compose del proyecto:

`docker-compose down -v `

Les dejo otro comando, por las dudas que no sea suficiente el anterior, que va a borrar **todas** las imágenes, contenedores y volúmenes que tengan, usenló con cuidado:

`docker system prune -a --volumes`


Una vez hecho eso, les recomiendo borrar los contenedores y reconstruir las imágenes.

Pueden correr:

`docker-compose build && docker-compose up`


Les recomiendo correrlo sin el `-d` al principio así pueden ver los logs más fácil en caso de que algo salga mal.

Luego de eso lo cancelan con `CTRL+C` y lo vuelven a levantar con `docker-compose up -d` o `docker-compose restart`. Luego para frenarlo, usan `docker-compose stop`

Presten **muchísima** atención a las variables de entorno y los valores que ponen. Yo les actualicé el .env.sample para que tengan de referencia. Ojo que les coincida con el `/init/create_schema.sql`, no llegué a configurar las variables de entorno.