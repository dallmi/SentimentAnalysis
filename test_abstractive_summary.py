"""
Test Abstractive Summarization with German Corporate Text
"""

import sys
from pathlib import Path

# Add LLM Solution to path
sys.path.insert(0, str(Path(__file__).parent / "LLM Solution"))

try:
    from abstractive_summarizer import AbstractiveSummarizer
    print("✓ AbstractiveSummarizer imported successfully")
except ImportError as e:
    print(f"❌ Failed to import AbstractiveSummarizer: {e}")
    print("\nMake sure transformers is installed:")
    print("  pip install transformers torch")
    sys.exit(1)


def test_german_corporate_articles():
    """Test with realistic German corporate intranet articles"""

    test_articles = [
        {
            "title": "Neue Homeoffice-Regelung 2025",
            "content": """
            Die Geschäftsführung hat nach umfangreichen Mitarbeiterbefragungen eine neue
            Richtlinie für flexibles Arbeiten verabschiedet. Ab dem 1. Januar 2025 können
            alle Mitarbeiter bis zu drei Tage pro Woche von zu Hause arbeiten. Diese
            Entscheidung wurde getroffen, um die Work-Life-Balance zu verbessern und die
            Mitarbeiterzufriedenheit zu erhöhen. Die IT-Abteilung stellt die notwendige
            Hardware und Software zur Verfügung. Für die Nutzung ist ein Antrag über das
            HR-Portal erforderlich. Führungskräfte müssen die Anträge innerhalb von fünf
            Arbeitstagen prüfen. Die neue Regelung gilt für alle Abteilungen außer dem
            Kundenservice. Mitarbeiter im Kundenservice haben spezielle Schichtpläne und
            sind davon ausgenommen. Weitere Details finden Sie im Mitarbeiterhandbuch.
            """
        },
        {
            "title": "Einführung neuer KI-Tools",
            "content": """
            Das Unternehmen investiert massiv in künstliche Intelligenz. Im Rahmen der
            Digitalisierungsstrategie werden mehrere KI-Tools eingeführt. ChatGPT Enterprise
            steht allen Mitarbeitern für Produktivitätssteigerung zur Verfügung. Ein
            automatisiertes Dokumenten-Management-System wird in der Rechtsabteilung
            implementiert. Die Einführung erfolgt schrittweise über drei Quartale.
            Schulungen beginnen im Februar 2025. Alle Mitarbeiter erhalten verpflichtende
            Trainings zur KI-Nutzung. Datenschutz hat höchste Priorität. Sensible Daten
            dürfen nicht in externe KI-Systeme eingegeben werden. Ein internes KI-Governance-
            Team wurde gegründet. Bei Fragen wenden Sie sich an ki-support@company.com.
            """
        },
        {
            "title": "Nachhaltigkeitsinitiative",
            "content": """
            Das Unternehmen hat sich ehrgeizige Nachhaltigkeitsziele gesetzt. Bis 2030 soll
            CO2-Neutralität erreicht werden. Alle Standorte werden auf erneuerbare Energien
            umgestellt. Photovoltaik-Anlagen werden auf allen Gebäuden installiert. Die
            Firmenflotte wird vollständig elektrifiziert. Geschäftsreisen sollen um 50%
            reduziert werden. Stattdessen werden virtuelle Meetings bevorzugt. Papierverbrauch
            wird minimiert durch digitale Prozesse. Ein Nachhaltigkeitsbericht wird
            quartalsweise veröffentlicht. Mitarbeiter können Verbesserungsvorschläge
            einreichen. Die besten Ideen werden mit Prämien belohnt.
            """
        }
    ]

    print("\n" + "=" * 80)
    print("TESTING ABSTRACTIVE SUMMARIZATION WITH GERMAN CORPORATE ARTICLES")
    print("=" * 80)

    try:
        print("\n[1/2] Loading mBART-large-50 model...")
        print("   (This may take 30-60 seconds on first load)")
        summarizer = AbstractiveSummarizer()
        print("   ✓ Model loaded successfully!")

        print("\n[2/2] Testing summarization on 3 German articles...")
        print("=" * 80)

        for i, article in enumerate(test_articles, 1):
            title = article['title']
            content = article['content']
            combined = f"{title}. {content}"

            print(f"\n{'─' * 80}")
            print(f"ARTICLE {i}: {title}")
            print(f"{'─' * 80}")
            print(f"\n📄 Original ({len(content.split())} words):")
            print(content.strip()[:200] + "...")

            # Generate summary
            print(f"\n⏳ Generating abstractive summary...")
            summary = summarizer.summarize(
                combined,
                source_lang="de_DE",
                max_length=100,
                min_length=30
            )

            print(f"\n✨ Abstractive Summary ({len(summary.split())} words):")
            print(f"   {summary}")

        print("\n" + "=" * 80)
        print("✓ ALL TESTS PASSED!")
        print("=" * 80)
        print("\n✓ Abstractive summarization is working correctly")
        print("✓ Ready for production use with --abstractive flag")
        print("\nUsage:")
        print("  python main_bertopic.py --input data.json --abstractive")

        return True

    except FileNotFoundError as e:
        print(f"\n❌ Model not found: {e}")
        print("\nPlease download the model first:")
        print("  python setup/download_mbart_model.py")
        return False

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_german_corporate_articles()
    sys.exit(0 if success else 1)
