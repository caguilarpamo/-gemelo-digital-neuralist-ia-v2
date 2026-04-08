from dotenv import load_dotenv
load_dotenv()  # Esto carga las variables desde el archivo .env

from graph.workflow import ejecutar_flujo

def main():

    print("===================================")
    print("💰 GEMELO DIGITAL FINANCIERO IA")
    print("===================================\n")

    req = input("Describe el sistema financiero: ")

    try:
        resultado = ejecutar_flujo(req)

        print("\n================ RESULTADO FINAL ================\n")

        print("\n📌 ANALISIS:\n")
        print(resultado["analisis"])

        print("\n🏗️ ARQUITECTURA:\n")
        print(resultado["arquitectura"])

        print("\n💻 CODIGO:\n")
        print(resultado["codigo"])

    except Exception as e:
        print("\n❌ ERROR:", str(e))


if __name__ == "__main__":
    main()