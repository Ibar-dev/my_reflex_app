import os

files = [
    "app/__init__.py",
    "app/app.py",
    "components/__init__.py",
    "components/header.py",
    "components/hero.py",
    "components/vehicle_selector.py",
    "components/benefits.py",
    "components/services.py",
    "components/faq.py",
    "components/contact.py",
    "components/footer.py",
    "state/__init__.py",
    "state/contact_state.py",
    "state/vehicle_state.py",
    "state/global_state.py",
    "utils/__init__.py",
    "utils/vehicle_data.py",
    "utils/email_service.py",
    "data/vehiculos_turismo.json",
    "assets/styles.css",
    "assets/selector-fix.css",
    "assets/images/bigstock-Technician-Is-Tuning-Engine-Ca-469398073.jpg",
    "assets/images/centralita-coche.jpg",
    "rxconfig.py",
    "requirements.txt"
]

print("Verificando archivos...\n")
missing = []
for f in files:
    exists = os.path.exists(f)
    status = "✅" if exists else "❌"
    print(f"{status} {f}")
    if not exists:
        missing.append(f)

print("\n" + "="*60)
if missing:
    print(f"❌ Faltan {len(missing)} archivos:")
    for f in missing:
        print(f"   - {f}")
else:
    print("✅ Todos los archivos están presentes")
