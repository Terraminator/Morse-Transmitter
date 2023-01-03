# morse transmitter
Sending and receiving morse signals via python

## light transmission
calculating resistance of led:
R=U/I ( Ohmsches Gesetz )

R=3.3V(output of pin)-2V(input of led) / I

R=1.3V/0.004A

R = 325Ohm -> 330 Ohm  

![image](https://github.com/Terraminator/Morse-Transmitter/blob/717114cba0968b9210b8442ad04d6a3351ccd1bb/Light_Transmission/image1.png)  


![image](https://gpiozero.readthedocs.io/en/stable/_images/pin_layout.svg)



Setup:
<pre>cd Light_Transmission</pre>  
<pre>pip install -r requirements.txt </pre>  

Usage of morse sender:  
<pre>python3 sender.py "message"</pre>  

Usage of morse receiver: 
<pre>python3 receiver.py</pre>  

documentation of functionality in Light_Transmission in german:  

Der Morse Transmitter basiert auf einer LED, welche an und abgeschaltet wird und einem Fotowiederstand(LDR), welcher an einen GPIO Pin eines Raspberry Pi angeschlossen ist.
Beim Senden einer Nachricht wird diese zunächst in Morse Code übersetzt (sender.encrypt) und an eine Instanz der Klasse Transmitter(transmitter.py) übergeben. Dieser hängt ein Trennungzeichen(SEPERATOR) and den Morse Code an, um die Checksum von der Nachricht zu seperieren.
Für jedes Signal in der Nachricht wird die LED für den Zeitraum transmitter.LONG bei "-" und für einen Zeitraum transmitter.SHORT bei "." aktiviert. Wenn nach einem Signal ein Abstand ist, wird nach dem aktivieren der LED diese für den Zeitraum transmitter.LONG abgeschaltet um die Buchstaben voneinander zu trennen andernfalls wird sie für den Zeitraum transmitter.SHORT deaktiviert um zwischen Signalen unterscheiden zu können.
Im Anschluss der Nachricht und dem Trennungszeichen z.B "HALLO WELT#" wird die Checksum gesendet. Diese Berechnet sich durch die Addition der Interpretation eines Zeichens in Form einer Zahl laut der Ascii Tabelle jedes Zeichens welches übermittelt wird.
Eine Vollständige Nachricht könnte zum Beispiel so aussehen: HALLO WELT#716 (.... .- .-.. .-.. --- /.-- . .-.. - #--... .---- -....).


Der Empfänger hingegen liest alle transmitter.delay_sleep sekunden den input pin des Fotowiderstands ab und speichert sie in einer Liste. Ein Leuchten der LED wird als "+" repräsentiert und Dunkelheit als "-". Sobald sich der Status des Pins ändert wird die Liste um ein neues Element erweitert.
Erst nachdem die ganze Nachricht in der Liste abgespeichert wurde, wird diese ausgewertet.
Beim Speichern wird ein input unter 0.3 als hell interpretiert und alles darüber als dunkel um weniger sensitiv gegenüber dem Umgebungslicht zu sein.
Man erhält durch dieses Vorgehen eine Liste wie diese: ['+++++', '-----', '+++++', '-----', '+++++', '-----', '+++++', '---------------', '+++++', '-----', '++++++++++', '---------------', '+++++', '-----', '++++++++++', '-----', '++++', '------', '+++++', '--------------', '++++++', '-----', '++++++++++', '-----', '++++', '-----', '++++++', '---------------', '+++++++++', '------', '+++++++++', '------', '+++++++++', '----------------', '+++++++++', '------', '++++', '-----', '+++++', '------', '+++++++++', '------', '++++', '---------------', '+++++', '------', '+++++++++', '-----', '++++++++++', '---------------', '+++++', '---------------', '+++++', '----', '++++++++++', '-----', '++++++', '-----', '++++', '---------------', '++++++++++', '---------------', '++++++++++', '-----', '++++++', '-----', '++++', '-----', '++++++++++', '-----', '++++++++++', '----------', '++++++++++', '-----', '++++++++++', '-----', '+++++', '------', '++++', '-----', '+++++', '----------------', '++++', '-----', '++++++++++', '-----', '++++++++++', '-----', '++++++++++', '-----', '++++++++++', '---------------', '++++++++++', '-----', '+++++', '-----', '++++', '------', '+++++', '-----', '++++']  

Zur Interpreation dieser werden drei Bereiche deklariert die durch transmitter.delay_sleep, transmitter.LONG sowie transmitter.SHORT berechnet werden.
z.B wäre bei der Standart Konfiguration "++++" als "." also kurzes signal zu interpretieren und ein "++++++++++" als "-" also langes Signal.
Ein neuer Buchstabe wird duch viele "---------------" erkennbar und die Trennung zwischen Signalen werden durch wenige "-----" gekennzeichnet.
Daraus folgt eine Morse Botschaft: z.B .... .- .-.. .-.. --- /.-- . .-.. - #--... .---- -.... was als HALLO WELT#716 übersetzt werden kann.
nach diese Interpretation wird die Botschaft in Checksum und Nachricht aufgeteilt und überprüft ob die übermittelte Botschaft mit der selbst ausgerechneten Checksum übereinstimmt.
Sollte dies nicht der Fall sein und die Checksum eine Zahl ist also vorraussichtlich richtig übermittelt wurde, wird versucht die Nachricht zu defragmentieren.
Hierbei wird eine Wortliste aus häufigen Wörtern mit den Unbekannten Wörtern der Nachricht verglichen und bei einer Levenshtein Distanz unter 5 als Kandidat in Betracht gezogen.
Wenn die Nachricht bei ersetzten eines unbekannten Wortes durch einen dieser Kandidaten die Checksum näher an die Übermittelte heranbringt wird dieses Wort durch den Kandidaten ersetzt.
Sollte nach Überprüfen aller möglichen Wörtern die erwartete Checksum erreicht wird, wird die defragmentierte Nachricht zurückgegeben, andernfalls wird die fragmentierte Nachricht ausgegeben und ein Fehler zurückgegeben.
In dem Fall, dass die Checksum vorraussichtlich falsch übertragen wurde, wird nicht versucht die Nachricht zu defragmentieren und ein Fehler wird zurückgegeben.
Wenn die Nachricht wie erwartet eintrifft wird diese zurückgegben.  


## audio transmission
