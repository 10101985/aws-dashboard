#!/usr/bin/env python3
"""
generar_dashboard.py
Consulta AWS y genera index.html con datos del stack
"""
import boto3
import json
from datetime import datetime, timedelta, timezone

REGION = 'sa-east-1'
INSTANCE_ID = 'i-02d98a9ed249b0dbe'
BUCKET = 'cristian-devops-bucket-2026'

def get_ec2_status():
    try:
        ec2 = boto3.client('ec2', region_name=REGION)
        r = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
        inst = r['Reservations'][0]['Instances'][0]
        state = inst['State']['Name']
        tipo = inst['InstanceType']
        return {
            'state': state,
            'type': tipo,
            'emoji': '✅' if state == 'running' else '⛔',
            'label': 'En línea' if state == 'running' else 'Detenido'
        }
    except:
        return {'state': 'unknown', 'emoji': '⚠️', 'label': 'Sin datos', 'type': '-'}

def get_s3_info():
    try:
        s3 = boto3.client('s3', region_name=REGION)
        r = s3.list_objects_v2(Bucket=BUCKET)
        objetos = r.get('Contents', [])
        total_bytes = sum(o['Size'] for o in objetos)
        total_kb = round(total_bytes / 1024, 1)
        return {
            'count': len(objetos),
            'size': f"{total_kb} KB",
            'status': '✅'
        }
    except:
        return {'count': 0, 'size': '0 KB', 'status': '⚠️'}

def get_cpu_metrics():
    try:
        cw = boto3.client('cloudwatch', region_name=REGION)
        ahora = datetime.now(timezone.utc)
        hace_3h = ahora - timedelta(hours=3)
        r = cw.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': INSTANCE_ID}],
            StartTime=hace_3h,
            EndTime=ahora,
            Period=3600,
            Statistics=['Average']
        )
        dp = r.get('Datapoints', [])
        if dp:
            avg = round(dp[-1]['Average'], 2)
            return {'value': f"{avg}%", 'status': '✅'}
        return {'value': 'Sin datos', 'status': '⚠️'}
    except:
        return {'value': 'Sin datos', 'status': '⚠️'}

def generar_html(ec2, s3, cpu):
    ahora = datetime.now().strftime('%d/%m/%Y %H:%M UTC')
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="1800">
    <title>AWS Dashboard — Cristian Robledo</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; padding: 2rem; }}
        header {{ text-align: center; margin-bottom: 2rem; }}
        header h1 {{ color: #00d4ff; font-size: 1.8rem; }}
        header p {{ color: #666; font-size: 0.85rem; margin-top: 0.5rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; max-width: 1000px; margin: 0 auto; }}
        .card {{ background: #0d0d1a; border: 1px solid #1a1a3e; border-radius: 12px; padding: 1.5rem; transition: border-color 0.3s; }}
        .card:hover {{ border-color: #00d4ff; }}
        .card .icon {{ font-size: 2rem; margin-bottom: 0.8rem; }}
        .card h3 {{ color: #a0a0c0; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; }}
        .card .value {{ font-size: 1.6rem; font-weight: bold; color: #ffffff; }}
        .card .sub {{ font-size: 0.85rem; color: #666; margin-top: 0.4rem; }}
        .status-ok {{ color: #00ff88; }}
        .status-warn {{ color: #ffaa00; }}
        .badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; margin-top: 0.5rem; }}
        .badge.online {{ background: #00331a; color: #00ff88; border: 1px solid #00ff88; }}
        .badge.offline {{ background: #330000; color: #ff4444; border: 1px solid #ff4444; }}
        footer {{ text-align: center; margin-top: 3rem; color: #333; font-size: 0.8rem; }}
        footer a {{ color: #00d4ff; text-decoration: none; }}
        .updated {{ text-align: center; color: #444; font-size: 0.8rem; margin-top: 1rem; }}
    </style>
</head>
<body>
    <header>
        <h1>⚡ AWS Infrastructure Dashboard</h1>
        <p>Cristian Robledo Macleood · Ingeniero en Informática · Cloud & DevOps</p>
    </header>

    <div class="grid">
        <div class="card">
            <div class="icon">🖥️</div>
            <h3>Servidor EC2</h3>
            <div class="value">{ec2['emoji']} {ec2['label']}</div>
            <div class="sub">Tipo: {ec2['type']} · sa-east-1</div>
            <span class="badge {'online' if ec2['state'] == 'running' else 'offline'}">{ec2['state']}</span>
        </div>

        <div class="card">
            <div class="icon">📦</div>
            <h3>Almacenamiento S3</h3>
            <div class="value">{s3['status']} {s3['count']} archivos</div>
            <div class="sub">Tamaño total: {s3['size']}</div>
            <span class="badge online">Activo</span>
        </div>

        <div class="card">
            <div class="icon">📊</div>
            <h3>CPU (últimas 3h)</h3>
            <div class="value">{cpu['status']} {cpu['value']}</div>
            <div class="sub">CloudWatch · AWS/EC2</div>
        </div>

        <div class="card">
            <div class="icon">🌐</div>
            <h3>Región AWS</h3>
            <div class="value" style="font-size:1.2rem;">América del Sur</div>
            <div class="sub">São Paulo · sa-east-1</div>
            <span class="badge online">Disponible</span>
        </div>

        <div class="card">
            <div class="icon">🐙</div>
            <h3>Portafolio</h3>
            <div class="value">12 proyectos</div>
            <div class="sub"><a href="https://github.com/10101985" target="_blank" style="color:#00d4ff;">github.com/10101985</a></div>
        </div>

        <div class="card">
            <div class="icon">🔄</div>
            <h3>Última actualización</h3>
            <div class="value" style="font-size:1rem;">{ahora}</div>
            <div class="sub">Actualización automática cada 30 min</div>
            <span class="badge online">GitHub Actions</span>
        </div>
    </div>

    <footer>
        <p>
            <a href="https://10101985.github.io/web-portfolio-personal" target="_blank">Portfolio</a> ·
            <a href="https://github.com/10101985" target="_blank">GitHub</a> ·
            <a href="https://linkedin.com/in/cristian-robledo-macleood-7538331b5" target="_blank">LinkedIn</a>
        </p>
    </footer>
</body>
</html>"""

    with open('index.html', 'w') as f:
        f.write(html)
    print(f"Dashboard generado exitosamente — {ahora}")

if __name__ == '__main__':
    print("Consultando AWS...")
    ec2 = get_ec2_status()
    s3 = get_s3_info()
    cpu = get_cpu_metrics()
    generar_html(ec2, s3, cpu)
    print(f"EC2: {ec2['label']} | S3: {s3['count']} archivos | CPU: {cpu['value']}")
