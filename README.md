# morse transmitter
Sending and receiving morse signals via a Raspberry Pi using light and sound


## light transmission

### demo video:
<a>https://youtu.be/I8XN870DwOY</a>

calculating resistance of led:
R=U/I ( Ohmsches Gesetz )

R=3.3V(output of pin)-2V(input of led) / I

R=1.3V/0.004A

R = 325Ohm -> 330 Ohm  


![image](https://gpiozero.readthedocs.io/en/stable/_images/pin_layout.svg)



Setup:
<pre>cd Light_Transmission</pre>  
<pre>pip install -r requirements.txt </pre>  

Usage of morse sender:  
<pre>python3 sender.py "message"</pre>  

Usage of morse receiver: 
<pre>python3 receiver.py</pre>  

documentation of functionality in Light_Transmission in german:  

Der Morse Transmitter basiert auf einer LED, welche an und abgeschaltet wird und einem Fotowiederstand (LDR), welcher an einen GPIO-Pin eines Raspberry Pi angeschlossen ist.
Beim Senden einer Nachricht wird diese zunächst in Morse Code übersetzt (sender.encrypt) und an eine Instanz der Klasse Transmitter(transmitter.py) übergeben. Dieser hängt ein Trennungszeichen (SEPERATOR) and den Morse Code an, um die Checksum von der Nachricht zu separieren.
Für jedes Signal in der Nachricht wird die LED für den Zeitraum transmitter.LONG bei "-" und für einen Zeitraum transmitter.SHORT bei "." aktiviert. Wenn nach einem Signal ein Abstand ist, wird nach dem Aktivieren der LED diese für den Zeitraum transmitter.LONG abgeschaltet, um die Buchstaben voneinander zu trennen andernfalls wird sie für den Zeitraum transmitter.SHORT deaktiviert, um zwischen Signalen unterscheiden zu können.
Im Anschluss der Nachricht und dem Trennungszeichen z.B "HALLO WELT#" wird die Checksum gesendet. Diese Berechnet sich durch die Addition der Interpretation eines Zeichens in Form einer Zahl laut der ASCII Tabelle jedes Zeichens, welches übermittelt wird.
Eine Vollständige Nachricht könnte zum Beispiel so aussehen: HALLO WELT#716 (.... .- .-.. .-.. --- /.-- . .-.. - #--... .---- -....).


Der Empfänger hingegen liest alle transmitter.delay_sleep Sekunden den Input Pin des Fotowiderstands ab und speichert sie in einer Liste. Ein Leuchten der LED wird als "+" repräsentiert und Dunkelheit als "-". Sobald sich der Status des Pins ändert, wird die Liste um ein neues Element erweitert.
Erst nachdem die ganze Nachricht in der Liste abgespeichert wurde, wird diese ausgewertet.
Beim Speichern wird ein Input unter 0.3 als hell interpretiert und alles darüber als dunkel um weniger sensitiv gegenüber dem Umgebungslicht zu sein.
Man erhält durch dieses Vorgehen eine Liste wie diese: ['+++++', '-----', '+++++', '-----', '+++++', '-----', '+++++', '---------------', '+++++', '-----', '++++++++++', '---------------', '+++++', '-----', '++++++++++', '-----', '++++', '------', '+++++', '--------------', '++++++', '-----', '++++++++++', '-----', '++++', '-----', '++++++', '---------------', '+++++++++', '------', '+++++++++', '------', '+++++++++', '----------------', '+++++++++', '------', '++++', '-----', '+++++', '------', '+++++++++', '------', '++++', '---------------', '+++++', '------', '+++++++++', '-----', '++++++++++', '---------------', '+++++', '---------------', '+++++', '----', '++++++++++', '-----', '++++++', '-----', '++++', '---------------', '++++++++++', '---------------', '++++++++++', '-----', '++++++', '-----', '++++', '-----', '++++++++++', '-----', '++++++++++', '----------', '++++++++++', '-----', '++++++++++', '-----', '+++++', '------', '++++', '-----', '+++++', '----------------', '++++', '-----', '++++++++++', '-----', '++++++++++', '-----', '++++++++++', '-----', '++++++++++', '---------------', '++++++++++', '-----', '+++++', '-----', '++++', '------', '+++++', '-----', '++++']
Zur Interpretation dieser werden drei Bereiche deklariert die durch transmitter.delay_sleep, transmitter.LONG sowie transmitter.SHORT berechnet werden.
z.B wäre bei der Standard Konfiguration "++++" als "." also kurzes Signal zu interpretieren und ein "++++++++++" als "-" also langes Signal.
Ein neuer Buchstabe wird durch viele "---------------" erkennbar und die Trennung zwischen Signalen werden durch wenige "-----" gekennzeichnet.
Daraus folgt eine Morse Botschaft: z.B .... .- .-.. .-.. --- /.-- . .-.. - #--... .---- -.... was als HALLO WELT#716 übersetzt werden kann.
nach dieser Interpretation wird die Botschaft in Checksum und Nachricht aufgeteilt und überprüft, ob die übermittelte Botschaft mit der selbst ausgerechneten Checksum übereinstimmt.
Sollte dies nicht der Fall sein und die Checksum eine Zahl ist also voraussichtlich richtig übermittelt wurde, wird versucht die Nachricht zu defragmentieren.
Hierbei wird eine Wortliste aus häufigen Wörtern mit den Unbekannten Wörtern der Nachricht verglichen und bei einer Levenshtein Distanz unter drei als das Wort als Kandidat für ein unbekanntes Wort in Betracht gezogen.

Wenn nach Überprüfen aller möglichen Wörter in allen Variationen die erwartete Checksum erreicht wird und keine unbekannten Wörter mehr in der Nachrricht vorhanden sind, wird die defragmentierte Nachricht zurückgegeben, andernfalls wird die fragmentierte Nachricht ausgegeben und ein Fehler zurückgegeben.
In dem Fall, dass die Checksum voraussichtlich falsch übertragen wurde, wird nicht versucht die Nachricht zu defragmentieren und ein Fehler wird zurückgegeben.
Wenn die Nachricht wie erwartet eintrifft wird diese zurückgegeben.

Die Konstanten transmitter.LONG und transmitter.SHORT können dynamisch nach oben erweitert aber nicht weiter reduziert werden ohne massive Fehler in der Übertragung auszulösen. Weiterhin ist zu beachten, dass transmitter.LONG doppelt so groß wie transmitter.SHORT sein sollte, um eine einwandfreie Unterscheidung zu gewährleisten.
Es ist zudem nicht möglich diese beiden Konstanten weiter zu verringern, und die Konstanten OFF_SHORT und OFF_LONG einzuführen, welche die übliche Größe von transmitter.LONG und transmitter.SHORT aufweisen.
Auch dies führt zur vollständigen Fehlübertragung der Nachricht.
Weiterhin ist es wichtig, dass transmitter.SEPERATOR nicht denselben Anfang von transmitter.EOB hat, da andernfalls transmitter.SEPERATOR andernfalls falsch interpretiert wird.
Die erwartete Zeit wird durch die gleiche Funktion wie in transmitter.send berechnet, danach wird diese Schätzung ein wenig erhöht um tendenziell eher zu viel Zeit als zu wenig zu schätzen.

Das Morse Verfahren ist anderen Verfahren in der Geschwindigkeit deutlich unterlegen, da diese z.B das Licht modulieren und so mehr Daten gleichzeitig senden können, auch die Hardware ist im Vergleich zu Glasfaser Technolgien oder ähnlichem eher langsam, da diese mit einer Verzögerung schaltet keine besonders starke Lichtquelle verwendet wird.
Jedoch wird dies ein Stück weit durch die Defragmentierung wieder wettgemacht, da eine Nachricht anhand einer Cheksum wiederhergestellt werden kann.



## audio transmission

Dieser Transmitter basiert auf eine Übertragung über Schall. Ein Schallsensor und aktiver Buzzer wird jeweils an einen Raspberry PI angeschlossen. Wie bei der
Übertragung durch Licht wird dabei erstmals die Nachricht nach der Eingabe in das Senderprogramm audiosender.py in Morse-Code verschlüsselt. Jeder Buchstabenfolge wird
ein "/" angehängt, Leerzeichen werden mit "|" ersetzt. Diese Zeichen stellen die verschiedenen Pausen dar.
Man kann die Geschwindigkeit eines kurzen Tones (Dit) in Millisekunden bestimmen, wovon alle anderen Tonlängen ermittelt werden. Lange Töne und Pausen zwischen
Buchstaben haben die dreifache, Pausen zwischen Wörtern die siebenfachewie Länge wie das eingegebene Tempo.
Damit der Empfänger die Geschwindigkeit ermitteln kann, wird jeder Nachricht die Startsequenz "|-.-.-/" hinzugefügt. Diese wird zur Kalibrierung des Empfängers genutzt.
Für jedes "." wird die Funktion shortsound(), für "-" longsound() abgerufen, welche den Buzzer für die vorher angegebene Zeit aktiviert.
Um die Töne zu unterscheiden wird nach jedem Signal eine Pause mit der Länge eines Dits durchgeführt.

Der Empfänger wartet anfangs, bis der Lautstärkepegel überschritten wird. Daraufhin wird ein Timer aktiviert, welcher so lange zählt, bis 
entweder der Pegel unter- oder später überschritten wird. Wenn dies geschieht wird in die Liste "sequence" der Wert des Timers eingetragen und er auf 0 gesetzt.
Diese Liste könnte entstehen: [65, 20, 24, 19, 57, 21, 17, 20, 67, 70, 20, 20, 20, 20, 20, 20, 20, 67, 18, 20, 59, 60, 18, 25, 59, 20, 21, 24, 13, 57, 24, 20, 65, 12, 
19, 21, 10, 56, 70, 20, 66, 20, 61, 22]  Es stellt diese Sequenz dar:    "-.-.-/..../.-/.-../.-../---"   -> HALLO
Die Aufnahme endet, wenn einige Zeit kein Ton empfangen wurde.

Die Interpretation der Liste kann nur stattfinden, wenn die Sendegeschwindigkeit bekannt ist. Dazu wird die Startsequenz genutzt, um die durchschnittliche Länge eines 
Dit zu ermitteln. Der Durchschnitt von den ersten zehn Elementen der Liste (Töne und Pausen) wird genommen, wobei lange Signale vorerst durch drei geteilt werden.
In dem aufgegührten Beispiel wäre die vom Programm genutzte Geschwindigkeit gerundet 21. Nun werden alle Werte in der Liste, welche ungefähr dieser Zahl entsprechen, auf
den selben Wert gebracht. Größere Werte werden auf das drei- oder siebenfache gerundet.
So würde die Liste nun aussehen: [62, 21, 21, 21, 62, 21, 62, 21, 62, 62, 21, 21, 21, 21, 21, 21, 21, 62, 21, 21, 62, 62, 21, 21, 62, 21, 21, 21, 21, 62, 21, 21, 62, 21, 
21, 21, 21, 62, 62, 21, 62, 21, 62, 21]
Als nächstes wird die Zahlenliste in den oben bereits aufgegriffenen String "..../.-/.-../.-../---" konvertiert und dabei die Startsequenz gelöscht. Dabei ist zu 
beachten, dass das erste Element
immer ein Ton ist. Das zweite Element ist daher garantiert eine Pause, das dritte ein Signal und so weiter.

Schlussendlich werden alle Zeichen so lange in einen seperaten String namens "letter" gegeben bis ein "/" oder "|" erkannt wird, um alle Buchstaben voneinander zu 
trennen. "letter" wird zurück in einen Buchstaben übersetzt, welcher der letzten Variable "decoded" hinzugefügt wird. Der String "letter" wird geleert. 
Dieses Verfahren wird so oft wiederholt bis alle Buchstaben übersetzt worden sind. Die Startsequenz wird ignoriert.
Falls die Sequenz falsch aufgenommen wurde und der Buchstabe nicht korrekt übersetzt werden kann wird eine Warnung ausgegeben und nach dem zweiten Zeichen des 
fragmentierten Buchstabens ein "/" eingefügt.

Wir sind auf besondere Probleme bei der Kalibrierung und korrekten Konfiguration des Audiosensors gestoßen. Den Ersten mussten wir tatsächlich wegen einem Defekt 
ersetzen. Der Ersatz hat zwar funktioniert, jedoch gab er bei einem Signal keine konstante Ausgabe, wodurch sie als viele kurze Töne und Pausen interpretiert wurde.
Um dies zu beheben, wird während der Tonaufnahme die Liste "last20" mit den letzten 20 Inputs gefüllt. Die unregelmäßigen Sequenzen werden geglättet, da nur eine 1 in 
dieser Liste enthalten sein muss, um es als Ton aufzunehmen.
Es gibt aber weiterhin die Gefahr, dass fehlerhafte Elemente in die Liste eingetragen werden. Daher werden alle Einträge, welche kleiner als 20 sind, gelöscht.

Leider verhindert diese Sicherheitsmaßnahme jedoch, hohe Geschwindigkeiten einzustellen.
Dieses Verfahren ist deutlich empfindlicher bei Störgeräuschen, da es kaum Defragmentierung besitzt, jedoch ist es auf die offiziellen Morse-Code Standards ausgelegt und passt sich automatisch an unterschiedliche Geschwindigkeiten an.
