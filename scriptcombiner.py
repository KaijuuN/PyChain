def combine_scripts_to_file(script_names, output_file):
    with open(output_file, 'w') as outfile:
        for filename in script_names:
            try:
                with open(filename, 'r') as infile:
                    # Schreibe den Dateinamen als Kommentar
                    outfile.write(f"# {filename}:\n")
                    # Kopiere den Inhalt des Skripts
                    outfile.write(infile.read())
                    # Füge eine neue Zeile nach jedem Skript hinzu
                    outfile.write("\n\n")
            except FileNotFoundError:
                print(f"Die Datei {filename} wurde nicht gefunden.")

# Beispielhafte Verwendung
script_names = ['main.py', 'block.py', 'blockchain.py','transactions.py','transactionpool.py', 'wallet.py', 'app.py']  # Manuelle Liste der Dateien
output_file_path = 'alle_scripte.txt'
combine_scripts_to_file(script_names, output_file_path)
