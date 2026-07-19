# AWS Infrastructure Dashboard 📊

Dashboard en vivo que muestra el estado de la infraestructura AWS,
generado automáticamente cada 2 horas con GitHub Actions y Python boto3.

## Ver en vivo
🔗 https://10101985.github.io/aws-dashboard

## Arquitectura
GitHub Actions (cada 2 horas)
→ Python + boto3 consulta AWS
→ Genera index.html con datos reales
→ Push automático a GitHub Pages
→ Dashboard actualizado en internet
## Datos mostrados
- Estado de instancia EC2 (running/stopped)
- Archivos en bucket S3 y tamaño total
- Métricas de CPU desde CloudWatch
- Región AWS activa

## Seguridad
Las credenciales AWS se almacenan como GitHub Secrets — nunca
aparecen en el código ni en el HTML generado.

## Tecnologías
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonaws&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![boto3](https://img.shields.io/badge/boto3-FF9900?style=flat&logo=amazonaws&logoColor=white)

## Autor
Cristian Robledo Macleood — [LinkedIn](https://www.linkedin.com/in/cristian-robledo-macleood-7538331b5/) | [Portfolio](https://10101985.github.io/web-portfolio-personal)
