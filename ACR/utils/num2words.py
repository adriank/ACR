#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ported from Delphi code at http://4programmers.net/Delphi/Gotowce/Zapis_słowny_liczby by Witold Filipczyk <witekfl@poczta.onet.pl>

def slow(t):
	J = (' ', ' jeden', ' dwa', ' trzy', ' cztery', ' pięć', ' sześć', ' siedem', ' osiem', ' dziewięć')
	N = (' dziesięć', ' jedenaście', ' dwanaście', ' trzynaście', ' czternaście', ' piętnaście',
	' szesnaście', ' siedemnaście', ' osiemnaście', ' dziewiętnaście')
	D = (' ', ' ' , ' dwadzieścia', ' trzydzieści', ' czterdzieści', ' pięćdziesiąt', ' sześćdziesiąt',
	' siedemdziesiąt', ' osiemdziesiąt', ' dziewięćdziesiąt')
	S = (' ', ' sto', ' dwieście', ' trzysta', ' czterysta', ' pięćset', ' sześćset', ' siedemset',
	' osiemset', ' dziewięćset')

	if t[1] == '1':
		return S[int(t[0])]+N[int(t[2])]
	else:
		return S[int(t[0])]+D[int(t[1])]+J[int(t[2])]

def liczba_slownie(liczba):
	G = ((' ',' ', ' '),
	(' tysiąc', ' tysiące', ' tysięcy'),
	(' milion', ' miliony', ' milionów'),
	(' miliard', ' miliardy', ' miliardów'),
	(' bilion', ' biliony', ' bilionów'),
	(' biliard', ' biliardy', ' biliardów'),
	(' trylion', ' tryliony', ' trylionów'),
	(' tryliard', ' tryliardy', ' tryliardów'))

	t = str(liczba)
	dl = len(t)
	sl = ''
	for i in range((dl - 1) // 3 + 1):
		t1 = t[-3:]
		t = t[:-3]
		#Wyrównanie do 3 cyfr
		for k in range(3 - len(t1)):
			t1 = '0' + t1
		#Jeżeli wszystkie 3 to 0 to nie ma po co dodawać nazwy grupy
		if t1 == '000':
			continue

		#Przypadek liczby pojedynczej}
		if t1 == '001':
			sl = slow(t1) + G[i][0] + sl
		else:
			#Liczby kończące się na 2, 3 lub 4 oprócz 12, 13 i 14. Ach ten język polski
			if t1[2] in ('2','3','4') and t1[1] != '1':
				sl = slow(t1) + G[i][1] + sl
			else:
				sl = slow(t1) + G[i][2] + sl
	return sl.replace('  ', ' ').strip()

if __name__ == "__main__":
	import sys
	print liczba_slownie(sys.argv[1])
