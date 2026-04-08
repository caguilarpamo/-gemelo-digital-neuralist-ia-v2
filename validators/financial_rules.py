def validar_codigo_financiero(code: str):

    errores = []

    if "float" in code:
        errores.append("❌ Uso de float en dinero")

    if "Decimal" not in code:
        errores.append("❌ No usa Decimal")

    if "transaction" not in code:
        errores.append("⚠️ No maneja transacciones")

    return errores if errores else ["✅ OK"]