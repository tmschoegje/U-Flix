#todo link to database more safely
#    question = get_object_or_404(Question, pk=question_id)
#!/usr/bin/env python
#-*- coding:utf-8 -*-


import numpy as np
import scipy.special as special

def FPvalue( *args):
    """ Return F an p value

    """
    df_btwn, df_within = __degree_of_freedom_( *args)

    mss_btwn = __ss_between_( *args) / float( df_btwn)   
    mss_within = __ss_within_( *args) / float( df_within)

    F = mss_btwn / mss_within    
    P = special.fdtrc( df_btwn, df_within, F)

    return( F, P)

def EffectSize( *args):
    """ Return the eta squared as the effect size for ANOVA

    """    
    return( float( __ss_between_( *args) / __ss_total_( *args)))

def __concentrate_( *args):
    """ Concentrate input list-like arrays

    """
    v = list( map( np.asarray, args))
    vec = np.hstack( np.concatenate( v))
    return( vec)

def __ss_total_( *args):
    """ Return total of sum of square

    """
    vec = __concentrate_( *args)
    ss_total = sum( (vec - np.mean( vec)) **2)
    return( ss_total)

def __ss_between_( *args):
    """ Return between-subject sum of squares

    """    
    # grand mean
    grand_mean = np.mean( __concentrate_( *args))

    ss_btwn = 0
    for a in args:
        ss_btwn += ( len(a) * ( np.mean( a) - grand_mean) **2)

    return( ss_btwn)

def __ss_within_( *args):
    """Return within-subject sum of squares

    """
    return( __ss_total_( *args) - __ss_between_( *args))

def __degree_of_freedom_( *args):
    """Return degree of freedom

       Output-
              Between-subject dof, within-subject dof
    """   
    args = list( map( np.asarray, args))
    # number of groups minus 1
    df_btwn = len( args) - 1

    # total number of samples minus number of groups
    df_within = len( __concentrate_( *args)) - df_btwn - 1

    return( df_btwn, df_within)

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import numpy as np 
import scipy.stats as st


from .models import Query, Result, InterviewSession, typeOrder, RandomisationOrder, Answer

def index(request):
	#latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return HttpResponse(render(request, 'uiquery/index.html'))
	
def experiment(request, sessionId, randomId):
	if randomId == 0:
		res = "&lt;ul class=&quot;searchResultsList&quot;&gt; &lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/20df1c69-e1bb-48f0-ab7a-1d9e6b14d496&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Vragenuur&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;28-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=ce1e9f62-678e-439e-9363-2809868d9a37&quot; target=&quot;_blank&quot;&gt;MV 1 Afval Canal Pride.docx&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Mondelinge vragen &lt;b&gt;Afval&lt;/b&gt; Canal Pride Eva van Esch, Partij voor de Dieren Op 16 juni jl. vond het feestelijke Canal Pride plaats, maar helaas was het zondag niet zo&rsquo;n feest voor het milieu.&lt;br&gt;Door het late opruimen is veel &lt;b&gt;afval&lt;/b&gt;, waaronder veel plastic, ballonnen en plastic confetti, van de kade in het water gewaaid.&lt;br&gt;Daardoor is het &lt;b&gt;afval&lt;/b&gt; verder verspreid, met alle gevolgen voor het milieu en dieren van dien.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/3fa29ef1-86d9-4c72-b3d7-f7d99652dcd6&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Raadsinformatiebijeenkomst&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;28-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=304eb7db-033c-4753-b74a-041d60dbd393&quot; target=&quot;_blank&quot;&gt;Raadsbrief Werkgelegenheid van de toekomst.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; &lsquo;&lt;b&gt;Afval&lt;/b&gt;&rsquo; is een grondstof en energie komt van duurzame bronnen.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=c6efbafe-c19a-4f92-9639-d8f238a7722c&quot; target=&quot;_blank&quot;&gt;Coalitieakkoord Utrecht ruimte voor iedereen.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; We stimuleren het hergebruik van grondstoffen in de bouwopgave en verbeteren de gescheiden inzameling van &lt;b&gt;afval&lt;/b&gt;.&lt;br&gt;&bull; We zetten volop in op circulariteit bij het sluiten van (nieuwe) contracten voor de verwerking van &lt;b&gt;afval&lt;/b&gt; en grondstoffen&lt;br&gt;Als we inwoners willen stimuleren &lt;b&gt;afval&lt;/b&gt; gescheiden in te zamelen is het belangrijk dat mensen tevreden zijn over de serviceverlening van de gemeente op dit gebied. 34Coalitieakkoord GroenLinks&thinsp;№&thinsp;D66&thinsp;№&thinsp;ChristenUnie Utrecht 2018-2022 &bull; Om de bovenstaande doelstellingen waar te maken nemen we als gemeente een regierol en maken we structureel extra middelen vrij voor het programma energie, oplopend tot totaal 6 miljoen euro per jaar. 2.4 Gezonde leefomgeving De parken, het water en de groenvoorzieningen bieden voor Utrechters een ideale gelegenheid om te ontspannen.&lt;br&gt;Uned) - 600 600 600 600 2.000 Doorgaande fietsroutes (o.a. tunnels, bruggen) - 400 750 750 750 2.500 Flexibel fonds knelpunten fietsroutes - 100 100 100 100 - Impuls straten 30 km/u - 250 500 500 500 1.000 Volledig duurzaam gemeentelijk vastgoed in 2040 130 260 460 590 720 730 Jongerenproject energietransitie Overvecht Noord - 100 100 - - - Maximaliseren circulair inkopen - - 500 500 500 500 Opschalen energietransitie 1.000 2.000 2.000 2.000 2.000 3.000 Uitvoeren visie Kanaalstraat en Amsterdamsestraatweg - - 1.100 1.100 1.100 1.100 Meer groene en blauwe verbindingen - 700 700 700 700 700 Toiletten M&aacute;xima- en Griftpark - - 68 68 68 68 Stapsgewijs invoeren stil asfalt - 50 100 100 100 100 Aanpak luchtkwaliteit 1.200 1.200 600 - - 1.000 Klimaatadaptatie - 150 150 - - - 49Coalitieakkoord GroenLinks&thinsp;№&thinsp;D66&thinsp;№&thinsp;ChristenUnie Utrecht 2018-2022 Utrecht: de kracht van iedereen 230 2.540 3.540 2.090 2.090 770 Utrecht maken we samen 2.0: buurtgesprekken en vernieuwen wijkparticipatie - 200 200 200 200 200 Matchen maatschappelijke initiatieven met vastgoed - 100 100 - - - Groene golf team voor initiatieven - 50 50 - - - Hogere versnelling Overvecht - 500 1.500 1.000 1.000 - Transparant werken, privacy, openbare en deelbare data - 800 800 - - - Informatiecommissaris - 70 70 70 70 70 Publieksdienstverlening op peil - 500 500 500 500 500 Uitbreiding B&amp;amp;W 230 320 320 320 320 - Totaal coalitieprogramma 3.110 18.628 28.203 22.003 21.768 21.480 Saldo 17.020 2.496 -15.221 -3.906 -388 - Aangepaste tabel Investeringsagenda Groei, tranche 2019 2019 2020 2021 2022 Investeringen sport 110 640 640 640 Investeringen welzijn 110 110 110 Investeringen onderwijs 190 680 680 680 Investeringen cultuur 100 70 70 170 Upgrade brug Merwedekanaal langs A12 100 100 1.000 Systeemsprong OV (v.a. 2023) U NED 1.000 1.000 Onverhaalbare kosten en plankosten MWKZ 900 1.000 1.000 1.000 Bruggen en woonboten 600 Beurskwartier-Lombokplein (v.a. 2023) Rondje Stadseiland 600 400 200 1.000 Plankosten USP/Rijnsweerd 500 - 300 300 Totaal 4.100 4.000 4.000 3.900 50Coalitieakkoord GroenLinks&thinsp;№&thinsp;D66&thinsp;№&thinsp;ChristenUnie Utrecht 2018-2022 Portefeuilleverdeling Lot van Hooijdonk Energie, mobiliteit, groen, dierenwelzijn Wijk Zuid en wijk West Kees Diepeveen Wonen, Merwedekanaalzone, grondzaken, openbare ruimte, Versnelling Overvecht, markten en havens Wijk Overvecht Linda Voortman Werk en inkomen, diversiteit (inclusief Utrecht zijn we samen), publieksdienstverlening, personeel en organisatie, onderzoek Wijk Zuidwest en wijk Noordoost Victor Everhardt (eerste loco-burgemeester) Volksgezondheid, milieu en emissieloos vervoer, jeugd en jeugdzorg, stationsgebied, vastgoed Wijk Leidsche Rijn Klaas Verschuure Ruimtelijke ontwikkeling, economische zaken, circulaire economie (inclusief &lt;b&gt;afval&lt;/b&gt;), mbo Wijk Noordwest Anke Klein Financi&euml;n, cultuur, onderwijs, wijkgericht werken en participatie, erfgoed, Het Utrechts Archief Wijk Oost en wijk Binnenstad Maarten van Ooijen Maatschappelijke ondersteuning, welzijn, asiel en integratie, sport Wijk Vleuten de Meern Informatie: www.utrecht.nl Utrecht, mei 2018&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=882b83f7-9a94-4392-b2ab-8ac716c522f8&quot; target=&quot;_blank&quot;&gt;Jaarstukken 2017.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Daarnaast zijn er onder de slogan 'Utrecht weet wat &lt;b&gt;afval&lt;/b&gt; waard is' diverse campagnes gevoerd om inwoners bewust te maken van de waarde van &lt;b&gt;afval&lt;/b&gt;.&lt;br&gt;Effectdoelstelling E2.3.1 Het &lt;b&gt;afval&lt;/b&gt; wordt in toenemende mate gescheiden ingezameld In de nota &lt;b&gt;Afval&lt;/b&gt; is Grondstof werd in 2015 tot de introductie van Het Nieuwe Inzamelen besloten.&lt;br&gt;Onder de slogan 'Utrecht weet wat &lt;b&gt;afval&lt;/b&gt; waard is' zijn in 2017 weer diverse campagnes gevoerd om inwoners bewust te maken van de waarde van &lt;b&gt;afval&lt;/b&gt;.&lt;br&gt;Hiermee zijn inwoners altijd op de hoogte van de actuele ophaaldagen van het &lt;b&gt;afval&lt;/b&gt; en kunnen zij informatie vinden over &lt;b&gt;afval&lt;/b&gt; scheiden.&lt;br&gt;Minder &lt;b&gt;afval&lt;/b&gt; en meer hergebruik van grondstoffen.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=f35f963d-91a6-473c-bd15-c88228bfdb49&quot; target=&quot;_blank&quot;&gt;Voorjaarsnota 2018 en 1e Berap 2018 (juni 2018).pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Programma: Openbare ruimte en groen (sub)doelstelling: 1.2 Het &lt;b&gt;afval&lt;/b&gt;- en hemelwater wordt veilig en milieuvriendelijk afgevoerd en de oppervlaktewaterkwaliteit voldoet aan de doelstellingen Was Wordt Subdoelstelling 1.2 Het &lt;b&gt;afval&lt;/b&gt;- en hemelwater wordt veilig en milieuvriendelijk afgevoerd en de waterkwaliteit is goed Subdoelstelling 1.2 Het &lt;b&gt;afval&lt;/b&gt;- en hemelwater wordt veilig en milieuvriendelijk ingezameld, en de oppervlaktewaterkwaliteit voldoet aan de doelstellingen.&lt;br&gt;E.1.2.1: Een goed functionerend rioolstelsel E.1.2.1: Een goed functionerend systeem voor de inzameling van &lt;b&gt;afval&lt;/b&gt;- en hemelwater en een hemelwaterbestendige openbare ruimte Nieuw: E1.2.X: De mate waarin de oppervlaktewaterkwaliteit voldoet aan de doelstellingen.&lt;br&gt; Het ondergronds &lt;b&gt;afval&lt;/b&gt; inzamelen is uitgesteld tot 2020 Vleuten de Meern In 2018 werkt de Parkorganisatie aan het tot stand komen van een definitief Programma van Eisen voor de ontwikkeling van een werkruimte annex bezoekerscentrum in het hart van het M&aacute;ximapark.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=c92c1ebb-59af-4789-a9e6-531635d96625&quot; target=&quot;_blank&quot;&gt;Bijlage 1 Antwoorden nagekomen schriftelijke vragen VJN 15 juni 2018.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Raadsvragencyclus Voorjaarsnota 2018, jaarstukken 2017 en meelopende raadsvoorstellen Nagekomen schriftelijke vragen: Vraagnummer: 444 Fractie: PVV Document naam: Jaarstukken Verbijzondering: ,&lt;b&gt;Afval&lt;/b&gt; wordt op effici&euml;nte wijze gescheiden&hellip;, Bladzijde (in pdf): 111 Portefeuillehouder(s): Klaas Verschuure Vraag: De hoeveelheid fijn restafval is in de laagbouwgebieden waar het nieuwe inzamelen is ingevoerd met 180 kilo per inwoner per jaar substantieel lager dan het stedelijk gemiddelde van 225 kilo per inwoner per jaar.&lt;br&gt;Antwoord: In de nota &lsquo;&lt;b&gt;Afval&lt;/b&gt; is Grondstof 2015-2018&rsquo; wordt weergegeven hoe Het Nieuwe Inzamelen in de wijken wordt ge&iuml;mplementeerd.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=1b0c9779-3fc3-4a59-afb2-32be96d37882&quot; target=&quot;_blank&quot;&gt;STVV Voorjaarsnota 2018 en 1e Berap 2018.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Programma: Openbare ruimte en groen (sub)doelstelling: 1.2 Het &lt;b&gt;afval&lt;/b&gt;- en hemelwater wordt veilig en milieuvriendelijk afgevoerd en de oppervlaktewaterkwaliteit voldoet aan de doelstellingen Was Wordt Subdoelstelling 1.2 Het &lt;b&gt;afval&lt;/b&gt;- en hemelwater wordt veilig en milieuvriendelijk afgevoerd en de waterkwaliteit is goed Subdoelstelling 1.2 Het &lt;b&gt;afval&lt;/b&gt;- en hemelwater wordt veilig en milieuvriendelijk ingezameld, en de oppervlaktewaterkwaliteit voldoet aan de doelstellingen.&lt;br&gt;E.1.2.1: Een goed functionerend rioolstelsel E.1.2.1: Een goed functionerend systeem voor de inzameling van &lt;b&gt;afval&lt;/b&gt;- en hemelwater en een hemelwaterbestendige openbare ruimte Nieuw:" + \
		" E1.2.X: De mate waarin de oppervlaktewaterkwaliteit voldoet aan de doelstellingen.&lt;br&gt; Het ondergronds &lt;b&gt;afval&lt;/b&gt; inzamelen is uitgesteld tot 2020 Vleuten de Meern In 2018 werkt de Parkorganisatie aan het tot stand komen van een definitief Programma van Eisen voor de ontwikkeling van een werkruimte annex bezoekerscentrum in het hart van het M&aacute;ximapark.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=64d583e7-3f5e-4023-b904-0c9eeafb4180&quot; target=&quot;_blank&quot;&gt;Bijlage 2 Antwoorden schriftelijke raadsvragen Coalitieakkoord.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; (zoals inkoop, &lt;b&gt;afval&lt;/b&gt;, energie) Antwoord: Onderwijsinstellingen zijn verantwoordelijk voor hun eigen bedrijfsvoering.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/37e5d134-0c6c-4795-abac-9f6f468ff483&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Mens en Samenleving&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;20-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=f35f963d-91a6-473c-bd15-c88228bfdb49&quot; target=&quot;_blank&quot;&gt;Voorjaarsnota 2018 en 1e Berap 2018 (juni 2018).pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Programma: Openbare ruimte en groen (sub)doelstelling: 1.2 Het &lt;b&gt;afval&lt;/b&gt;- en hemelwater wordt veilig en milieuvriendelijk afgevoerd en de oppervlaktewaterkwaliteit voldoet aan de doelstellingen Was Wordt Subdoelstelling 1.2 Het &lt;b&gt;afval&lt;/b&gt;- en hemelwater wordt veilig en milieuvriendelijk afgevoerd en de waterkwaliteit is goed Subdoelstelling 1.2 Het &lt;b&gt;afval&lt;/b&gt;- en hemelwater wordt veilig en milieuvriendelijk ingezameld, en de oppervlaktewaterkwaliteit voldoet aan de doelstellingen.&lt;br&gt;E.1.2.1: Een goed functionerend rioolstelsel E.1.2.1: Een goed functionerend systeem voor de inzameling van &lt;b&gt;afval&lt;/b&gt;- en hemelwater en een hemelwaterbestendige openbare ruimte Nieuw: E1.2.X: De mate waarin de oppervlaktewaterkwaliteit voldoet aan de doelstellingen.&lt;br&gt; Het ondergronds &lt;b&gt;afval&lt;/b&gt; inzamelen is uitgesteld tot 2020 Vleuten de Meern In 2018 werkt de Parkorganisatie aan het tot stand komen van een definitief Programma van Eisen voor de ontwikkeling van een werkruimte annex bezoekerscentrum in het hart van het M&aacute;ximapark.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/37e5d134-0c6c-4795-abac-9f6f468ff483&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Mens en Samenleving&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;20-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=c6efbafe-c19a-4f92-9639-d8f238a7722c&quot; target=&quot;_blank&quot;&gt;Coalitieakkoord Utrecht ruimte voor iedereen.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; We stimuleren het hergebruik van grondstoffen in de bouwopgave en verbeteren de gescheiden inzameling van &lt;b&gt;afval&lt;/b&gt;.&lt;br&gt;&bull; We zetten volop in op circulariteit bij het sluiten van (nieuwe) contracten voor de verwerking van &lt;b&gt;afval&lt;/b&gt; en grondstoffen&lt;br&gt;Als we inwoners willen stimuleren &lt;b&gt;afval&lt;/b&gt; gescheiden in te zamelen is het belangrijk dat mensen tevreden zijn over de serviceverlening van de gemeente op dit gebied. 34Coalitieakkoord GroenLinks&thinsp;№&thinsp;D66&thinsp;№&thinsp;ChristenUnie Utrecht 2018-2022 &bull; Om de bovenstaande doelstellingen waar te maken nemen we als gemeente een regierol en maken we structureel extra middelen vrij voor het programma energie, oplopend tot totaal 6 miljoen euro per jaar. 2.4 Gezonde leefomgeving De parken, het water en de groenvoorzieningen bieden voor Utrechters een ideale gelegenheid om te ontspannen.&lt;br&gt;Uned) - 600 600 600 600 2.000 Doorgaande fietsroutes (o.a. tunnels, bruggen) - 400 750 750 750 2.500 Flexibel fonds knelpunten fietsroutes - 100 100 100 100 - Impuls straten 30 km/u - 250 500 500 500 1.000 Volledig duurzaam gemeentelijk vastgoed in 2040 130 260 460 590 720 730 Jongerenproject energietransitie Overvecht Noord - 100 100 - - - Maximaliseren circulair inkopen - - 500 500 500 500 Opschalen energietransitie 1.000 2.000 2.000 2.000 2.000 3.000 Uitvoeren visie Kanaalstraat en Amsterdamsestraatweg - - 1.100 1.100 1.100 1.100 Meer groene en blauwe verbindingen - 700 700 700 700 700 Toiletten M&aacute;xima- en Griftpark - - 68 68 68 68 Stapsgewijs invoeren stil asfalt - 50 100 100 100 100 Aanpak luchtkwaliteit 1.200 1.200 600 - - 1.000 Klimaatadaptatie - 150 150 - - - 49Coalitieakkoord GroenLinks&thinsp;№&thinsp;D66&thinsp;№&thinsp;ChristenUnie Utrecht 2018-2022 Utrecht: de kracht van iedereen 230 2.540 3.540 2.090 2.090 770 Utrecht maken we samen 2.0: buurtgesprekken en vernieuwen wijkparticipatie - 200 200 200 200 200 Matchen maatschappelijke initiatieven met vastgoed - 100 100 - - - Groene golf team voor initiatieven - 50 50 - - - Hogere versnelling Overvecht - 500 1.500 1.000 1.000 - Transparant werken, privacy, openbare en deelbare data - 800 800 - - - Informatiecommissaris - 70 70 70 70 70 Publieksdienstverlening op peil - 500 500 500 500 500 Uitbreiding B&amp;amp;W 230 320 320 320 320 - Totaal coalitieprogramma 3.110 18.628 28.203 22.003 21.768 21.480 Saldo 17.020 2.496 -15.221 -3.906 -388 - Aangepaste tabel Investeringsagenda Groei, tranche 2019 2019 2020 2021 2022 Investeringen sport 110 640 640 640 Investeringen welzijn 110 110 110 Investeringen onderwijs 190 680 680 680 Investeringen cultuur 100 70 70 170 Upgrade brug Merwedekanaal langs A12 100 100 1.000 Systeemsprong OV (v.a. 2023) U NED 1.000 1.000 Onverhaalbare kosten en plankosten MWKZ 900 1.000 1.000 1.000 Bruggen en woonboten 600 Beurskwartier-Lombokplein (v.a. 2023) Rondje Stadseiland 600 400 200 1.000 Plankosten USP/Rijnsweerd 500 - 300 300 Totaal 4.100 4.000 4.000 3.900 50Coalitieakkoord GroenLinks&thinsp;№&thinsp;D66&thinsp;№&thinsp;ChristenUnie Utrecht 2018-2022 Portefeuilleverdeling Lot van Hooijdonk Energie, mobiliteit, groen, dierenwelzijn Wijk Zuid en wijk West Kees Diepeveen Wonen, Merwedekanaalzone, grondzaken, openbare ruimte, Versnelling Overvecht, markten en havens Wijk Overvecht Linda Voortman Werk en inkomen, diversiteit (inclusief Utrecht zijn we samen), publieksdienstverlening, personeel en organisatie, onderzoek Wijk Zuidwest en wijk Noordoost Victor Everhardt (eerste loco-burgemeester) Volksgezondheid, milieu en emissieloos vervoer, jeugd en jeugdzorg, stationsgebied, vastgoed Wijk Leidsche Rijn Klaas Verschuure Ruimtelijke ontwikkeling, economische zaken, circulaire economie (inclusief &lt;b&gt;afval&lt;/b&gt;), mbo Wijk Noordwest Anke Klein Financi&euml;n, cultuur, onderwijs, wijkgericht werken en participatie, erfgoed, Het Utrechts Archief Wijk Oost en wijk Binnenstad Maarten van Ooijen Maatschappelijke ondersteuning, welzijn, asiel en integratie, sport Wijk Vleuten de Meern Informatie: www.utrecht.nl Utrecht," + \
		" mei 2018&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt; &lt;/ul&gt;"
		quest = "Wat zijn de doelstellingen om het verwerken van afval te verbeteren en recycling the promoten?"
		f = 0
		manualqId = 0
	elif randomId == 1:
		res = "&lt;ul class=&quot;searchResultsList&quot;&gt; &lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=f40eeb71-bcf9-4697-877d-066f354dd5cf&quot; target=&quot;_blank&quot;&gt;Meerjaren Perspectief Bereikbaarheid (juni 2018).pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Zo zijn er in 2017 tien projecten uitgevoerd die de &lt;b&gt;verkeersveiligheid&lt;/b&gt; verbeteren.&lt;br&gt;fietscursussen voor diverse doelgroepen), gedragsbe&iuml;nvloeding (snelheidsdisplays) en handhaving (fietsverlichtingsacties) verbeteren we de &lt;b&gt;verkeersveiligheid&lt;/b&gt;.&lt;br&gt;, &lt;b&gt;Verkeersveiligheid&lt;/b&gt;, De Gebruiker Centraal, Goederenvervoer en Schoon Vervoer.&lt;br&gt;Actieplan &lt;b&gt;Verkeersveiligheid&lt;/b&gt; Het huidige budget is voldoende voor uitvoering van de lopende projecten en programmakosten in 2018.&lt;br&gt;Het gaat hier om mobiliteitsmanagement, verkeersmanagement, logistiek, smart mobility, &lt;b&gt;verkeersveiligheid&lt;/b&gt; en schoon vervoer.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=febc75e1-4386-4189-8d0d-3141e3fa54f6&quot; target=&quot;_blank&quot;&gt;Voorstel_9778.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Voor de komende 1 of 2 jaar kan het werk worden voortgezet op de steeds belangrijkere werkvelden Slim regelen, &lt;b&gt;Verkeersveiligheid&lt;/b&gt;, Smart Mobility en Schoon Vervoer. 1.3 In het MPB wordt rekening gehouden met het waarschijnlijk vervallen van provinciale subsidies.&lt;br&gt;Het gaat hierbij onder meer om: ▪ Herinrichting van winkel- en verblijfsstraten waar regelmatig met de buurt al eerste stappen zijn gezet in de participatie (Kanaalstraat, As Votulast, 2de fase Amsterdamsestraatweg) ▪ Maatregelen die (bij voorkeur) meeliften met andere projecten (Moldaudreef met NRU, fietspad Waterlinieweg met bouwplannen Opaalweg) ▪ Langduriger budget voor de steeds belangrijker wordende werkvelden &lt;b&gt;verkeersveiligheid&lt;/b&gt;, slim regelen (verkeers- en mobiliteitsmanagement en logistiek) en smart mobility (met dit MPB slechts budget voor twee jaar) ▪ Mogelijke verdere stappen voor invoering van snorfietsen op de rijbaan (zie raadsbrief van 3 januari 2018 Luchtkwaliteit en gezondheid) ▪ (Verkenningen naar) nieuwe of aan te passen fietsbruggen en -tunnels (fietstunnel 2e &ndash; 1e Daalsedijk, Demkabrug, Demkabrug / brug Zuilen &ndash; Lage Weide). 1.2 Met dit MPB 2018 wordt slechts een beperkte extra stap gezet in het bereiken van de hoge ambities op het gebied van mobiliteit.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=99893d74-f5c0-4cae-af30-c68bcc4c362e&quot; target=&quot;_blank&quot;&gt;STVV Raadsvoorstel MPSO 2018 en MPB 2018.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Voor de komende 1 of 2 jaar kan het werk worden voortgezet op de steeds belangrijkere werkvelden Slim regelen, &lt;b&gt;Verkeersveiligheid&lt;/b&gt;, Smart Mobility en Schoon Vervoer. 1.3 In het MPB wordt rekening gehouden met het waarschijnlijk vervallen van provinciale subsidies.&lt;br&gt;Het gaat hierbij onder meer om: ▪ Herinrichting van winkel- en verblijfsstraten waar regelmatig met de buurt al eerste stappen zijn gezet in de participatie (Kanaalstraat, As Votulast, 2de fase Amsterdamsestraatweg) ▪ Maatregelen die (bij voorkeur) meeliften met andere projecten (Moldaudreef met NRU, fietspad Waterlinieweg met bouwplannen Opaalweg) ▪ Langduriger budget voor de steeds belangrijker wordende werkvelden &lt;b&gt;verkeersveiligheid&lt;/b&gt;, slim regelen (verkeers- en mobiliteitsmanagement en logistiek) en smart mobility (met dit MPB slechts budget voor twee jaar) ▪ Mogelijke verdere stappen voor invoering van snorfietsen op de rijbaan (zie raadsbrief van 3 januari 2018 Luchtkwaliteit en gezondheid) ▪ (Verkenningen naar) nieuwe of aan te passen fietsbruggen en -tunnels (fietstunnel 2e &ndash; 1e Daalsedijk, Demkabrug, Demkabrug / brug Zuilen &ndash; Lage Weide). 1.2 Met dit MPB 2018 wordt slechts een beperkte extra stap gezet in het bereiken van de hoge ambities op het gebied van mobiliteit.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=01c9b010-8291-40f0-9815-c2380578e50e&quot; target=&quot;_blank&quot;&gt;Bijlage 3 Tweede erratum Jaarstukken 2017.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Dit door middel van de voorziening de Taalschool waar nieuwkomers (leerlingen in het PO) de Nederlandse taal leren zodat zij na ca. 1&frac12; jaar Taalschool bij uitstroom naar het reguliere onderwijs Nederlands spreken, lezen en schrijven &ndash; passend bij het vastgestelde uitstroomniveau. 614 614 0 Verkeersexamen in de wijken Resultaat &lt;b&gt;Verkeersveiligheid&lt;/b&gt; PO&amp;nbsp; groep 7/8 afsluiten met theoretisch en praktisch &amp;nbsp;examen 30 32 -2 Schoolmaatschappelijk werk PO Leerlingen ondersteunen bij achterstanden in hun ontwikkeling op school (Buurtteams) 1.203 1.198 5 Overgang PO naar VO Het realiseren van de beoogde effecten conform de Beleidsregel Onderwijs Utrecht, Goed onderwijs voor elk kind, binnen het thema Schoolloopbaan 12-23. 205 205 0 Leerlingenbegeleiding PO Het realiseren van de beoogde effecten conform de Beleidsregel Onderwijs Utrecht 2015, Goed onderwijs voor elk kind, binnen het thema Zorg 0-12. 1.031 1.033 -2 Onderwijsondersteuning woonwagen- en Romaleerlingen Leerlingen ondersteunen bij achterstanden in hun ontwikkeling op school 88 88 0 Conci&euml;rges PO Leerlingen en personeel voelen zich veilig in en rondom de school 276 267 9 Combinatiefuncties onderwijs, activiteiten brede talentontwikkeling en programma Brede Scholen Het realiseren van de beoogde effecten conform de Beleidsregel Onderwijs Utrecht, Goed onderwijs voor elk kind, binnen het thema Talentontwikkeling 0-12.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=c6efbafe-c19a-4f92-9639-d8f238a7722c&quot; target=&quot;_blank&quot;&gt;Coalitieakkoord Utrecht ruimte voor iedereen.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; We investeren structureel in de verbetering van de &lt;b&gt;verkeersveiligheid&lt;/b&gt; en verliezen dit in de hele stad niet uit het oog bij alles wat we doen.&lt;br&gt;Dat draagt ook bij aan de &lt;b&gt;verkeersveiligheid&lt;/b&gt; van fietsers en voetgangers&lt;br&gt;&bull; Bij de uitvoering van verkeersmaatregelen, verkeersmanagement en herinrichtingsplannen kiezen we de meest effectieve maatregel om bereikbaarheid en &lt;b&gt;verkeersveiligheid&lt;/b&gt; te verbeteren.&lt;br&gt;We maken structureel middelen vrij om de &lt;b&gt;verkeersveiligheid&lt;/b&gt; in Utrecht te verbeteren.&lt;br&gt;Daarbij kijken we vooral naar noodzakelijke verdere intensiveringen gekoppeld aan de opgaven en naar zaken die incidenteel zijn geregeld, maar structureel aandacht vragen. 47Coalitieakkoord GroenLinks&thinsp;№&thinsp;D66&thinsp;№&thinsp;ChristenUnie Utrecht 2018-2022 In onderstaande tabel is de financi&euml;le uitwerking van dit coalitieakkoord verwerkt: Financieel beeld coalitieprogramma Baten 2018 2019 2020 2021 2022 Structureel Financi&euml;le ruimte voorjaarsnota 2018 16.472 1.109 4.952 10.417 13.650 13.650 Aanvullende financi&euml;le ruimte 3.658 20.015 8.030 7.680 7.730 7.830 Bestedings- en dekkingsvoorstellen 3.658 Inzet fonds innovatie Sociaal Domein voor maatregelen armoede, schulden en sociale basis 4.000 Inzet restant middelen huishoudelijke hulp toeslag 2.000 Inzet reserve grondexploitatie 6.300 Budget culturele voorziening Leidsche Rijn tot aan realisatie 900 550 Inzet stille reserves voor weerstandsvermogen 470 Actualisatie accres 800 800 800 800 Efficiency organisatie 425 425 975 1.025 1.125 Inzet budgetten gekoppeld aan opgaven 660 660 660 660 660 Vergroening brandstofmotoren in liggeld 80 115 165 165 165 Parkeren: aanpassing tarieven kort parkeren 1.600 1.600 1.600 1.600 1.600 Parkeren: aanpassing vergunningen A1 &amp;amp; A2 600 600 600 600 600 Parkeren: handhaven (scanauto&rsquo;s) 200 500 500 500 500 Inzet verhoging en groei toeristenbelasting voor groei evenementen 1.280 1.280 880 880 880 OZB indexering conform spelregel 1,5% 1.500 1.500 1.500 1.500 1.500 Totaal financi&euml;le ruimte 20.130 21.124 12.982 18.097 21.380 21.480 Lasten 2018 2019 2020 2021 2022 Structureel Utrecht: plaats van iedereen 200 7.800 11.965 8.955 8.590 5.712 Utrechtse Onderwijsagenda (aanpak lerarentekort, talentontwikkeling, kansengelijkheid, aanpak mismatch onderwijs-arbeidsmarkt) - 650 650 410 400 650 In stand houden kwaliteit en infrastructuur onderwijs achterstandenbeleid - - 2.000 2.200 2.400 2.600 Verbeteren en uitbreiden maatschappelijke stages - 50 50 50 50 50 Regionaal Investeringsplatform - - 3.000 - - - Investeren in ecosysteem voor starters en groeiers - 750 750 500 500 500 Fonds Mismatch Arbeidsmarkt - 1.000 500 500 500 - Omgevingsvisie Binnenstad 200 200 - - - - Voortzetten evenementenbeleid - 440 300 300 300 300 Vuelta 2020 - 800 - - - - Castellum Hoge Woerd (vanaf 2020 in groeikader verwerken) - 100 - - - - Jongerencultuurhuis Overvecht - 220 200 200 200 200 Religieus Cultureel Erfgoed - - 50 75 75 75 Armoederegelingen - 500 500 500 500 500 48Coalitieakkoord GroenLinks&thinsp;№&thinsp;D66&thinsp;№&thinsp;ChristenUnie Utrecht 2018-2022 Maatschappelijke initiatieven armoedebeleid - 100 100 100 100 - Impuls buurtgerichte vroegsignalering schulden - 300 400 500 500 - Voorkomen van schulden en innoveren schuldhulpverlening voor jongeren en ZZP&rsquo;ers. - 300 400 500 - - Begroot effect schuldenaanpak - - - 200 -300 -500 -500 Pilot huurverlaging 500 500 - - - Bijdrage studenten met een functiebeperking - 140 140 140 285 285 Voedselbanken meer zekerheid op langdurig gebruik van lokaties - 150 150 150 150 150 Flexibel, snel in te zetten budget tbv acute knelpunten toegankelijkheid, looproutes Solgu - 275 275 275 275 - Utrecht Zijn We Samen: anti discriminatie agenda - - 150 150 150 - Utrecht Zijn We Samen: tegengaan polarisatie en radicalisering - - 250 570 570 - Tegengaan laaggeletterdheid, vergroten digivaardigheden - 250 250 250 250 250 Onderzoek extra zwembad - 25 - - - - Buurtpacten (samenwerking partijen, voorkomen overbelasting mantelzorgers) - 100 50 - - - Versterken Sociale Basis Jeugd en JGZ ter voorkoming van wachtlijsten - 500 500 500 500 - Voortzetten en intensiveren aanpak ondermijning - 250 250 635 635 - Voortzetten extra inzet wijk BOA&rsquo;s en Toezicht &amp;amp; Handhaving &lsquo;s nachts - - 550 550 550 550 Ketenregisseur voorkomen mensenhandel - 100 100 100 100 100 Voorkomen misbruik minderjarigen in de seksindustrie, aanbod uitstapprogramma&rsquo;s. - 100 100 100 100 - Utrecht: nieuwe energie van iedereen 2.680 8.288 12.698 10.958 11.088 14.998 Versnellingsaanpak wonen - 500 500 - - - Nieuwe woonconcepten 508 500 500 500 - Aanpak Huisjesmelkers - 520 520 - - - Mobiliteit voor iedereen (fietslessen, fiets in U-pas) 50 50 50 50 50 50 Voortzetten koers " + \
		"SRSRSB, verbinden mobiliteit met binnenstedelijke ontwikkelingen (groen licht voor de fiest, nieuwe mobiliteitsdiensten, uitbreiding laadpalen) 300 900 2.150 2.150 2.150 1.000 Aanpak &lt;b&gt;verkeersveiligheid&lt;/b&gt; - - 1.250 1.250 1.250 1.250 Schaalsprong mobiliteit (o.a.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=54de13ae-4975-43d9-ab22-20eb65f8af7b&quot; target=&quot;_blank&quot;&gt;Subsidiestaat Gemeente Utrecht 2018.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Dit door middel van de voorziening de Taalschool waar nieuwkomers (leerlingen in het PO) de Nederlandse taal leren zodat zij na ca. 1&frac12; jaar Taalschool bij uitstroom naar het reguliere onderwijs Nederlands spreken, lezen en schrijven &ndash; passend bij het vastgestelde uitstroomniveau. 614 614 Verkeersexamen in de wijken Resultaat &lt;b&gt;Verkeersveiligheid&lt;/b&gt; PO&amp;nbsp; groep 7/8 afsluiten met theoretisch en praktisch &amp;nbsp;examen 30 Schoolmaatschappelijk werk PO Leerlingen ondersteunen bij achterstanden in hun ontwikkeling op school (Buurtteams) 1.225 1.225 Overgang PO naar VO Het realiseren van de beoogde effecten conform de Beleidsregel Onderwijs Utrecht, Goed onderwijs voor elk kind, binnen het thema Schoolloopbaan 12-23. 209 209 Leerlingenbegeleiding PO Het realiseren van de beoogde effecten conform de Beleidsregel Onderwijs Utrecht 2015, Goed onderwijs voor elk kind, binnen het thema Zorg 0-12. 1.213 1.213 Totaal programma Werk en Inkomen Prestatiedoelstelling programmabegroting 2018 Subsidiedoelstelling Omschrijving subsidiedoelstelling Begroting 2018 Waarvan &quot;vaste&quot; verlening met jaarsubsidies Meerjarig verleend ten laste van 2018 Onderwijsondersteuning woonwagen- en Romaleerlingen PO Leerlingen ondersteunen bij achterstanden in hun ontwikkeling op school 90 90 Conci&euml;rges PO Leerlingen en personeel voelen zich veilig in en rondom de school 281 281 Combinatiefuncties onderwijs, activiteiten brede talentontwikkeling en programma Brede Scholen Het realiseren van de beoogde effecten conform de Beleidsregel Onderwijs Utrecht, Goed onderwijs voor elk kind, binnen het thema Talentontwikkeling 0-12.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=64d583e7-3f5e-4023-b904-0c9eeafb4180&quot; target=&quot;_blank&quot;&gt;Bijlage 2 Antwoorden schriftelijke raadsvragen Coalitieakkoord.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Fractie: CDA Document naam: coalitieakkoord Bladzijde: 27 Portefeuillehouder(s): Lot van Hooijdonk Vraag: Het inzetten op fietsers en voetgangers is duidelijk, maar hoe wil het college de &lt;b&gt;verkeersveiligheid&lt;/b&gt; verbeteren?&lt;br&gt;Valt daar de hele voormalige portefeuille verkeer (inclusief &lt;b&gt;verkeersveiligheid&lt;/b&gt;) onder?&lt;br&gt;Antwoord: Mobiliteit omvat inderdaad ook verkeer en de voormalig portefeuille Bereikbaarheid (inclusief &lt;b&gt;verkeersveiligheid&lt;/b&gt;).&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=816a8443-9ea6-4301-8584-585c607dda73&quot; target=&quot;_blank&quot;&gt;Subsidiestaat Gemeente Utrecht 2019.pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Dit door middel van de voorziening de Taalschool waar nieuwkomers (leerlingen in het PO) de Nederlandse taal leren zodat zij na ca. 1&frac12; jaar Taalschool bij uitstroom naar het reguliere onderwijs Nederlands spreken, lezen en schrijven &ndash; passend bij het vastgestelde uitstroomniveau. 364 364 Verkeersexamen in de wijken Resultaat &lt;b&gt;Verkeersveiligheid&lt;/b&gt; PO&amp;nbsp; groep 7/8 afsluiten met theoretisch en praktisch &amp;nbsp;examen 30 Schoolmaatschappelijk werk PO (subsidietender Buurtteam Jeugd) Leerlingen ondersteunen bij achterstanden in hun ontwikkeling op school (Buurtteams) 1.203 1.203 Overgang PO naar VO Het realiseren van de beoogde effecten conform de Beleidsregel Onderwijs Utrecht, Goed onderwijs voor elk kind, binnen het thema Schoolloopbaan 12-23. 209 209 Onderwijsondersteuning woonwagen- en Romaleerlingen PO Leerlingen ondersteunen bij achterstanden in hun ontwikkeling op school 90 90 Conci&euml;rges PO Leerlingen en personeel voelen zich veilig in en rondom de school 281 281 Totaal programma Werk en Inkomen Prestatiedoelstelling programmabegroting 2019 Subsidiedoelstelling Omschrijving subsidiedoelstelling Begroting 2019 Waarvan &quot;vaste&quot; verlening met jaarsubsidies Meerjarig verleend ten laste van 2019 Combinatiefuncties onderwijs, activiteiten brede talentontwikkeling en programma Brede Scholen Het realiseren van de beoogde effecten conform de Beleidsregel Onderwijs Utrecht, Goed onderwijs voor elk kind, binnen het thema Talentontwikkeling 0-12.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=f35f963d-91a6-473c-bd15-c88228bfdb49&quot; target=&quot;_blank&quot;&gt;Voorjaarsnota 2018 en 1e Berap 2018 (juni 2018).pdf&lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Intensiveringen 2018 2019 2020 2021 2022 Utrecht: plaats van iedereen 200 7.800 12.165 9.255 9.090 Utrecht: nieuwe energie van iedereen 2.680 8.288 12.698 10.958 11.088 Utrecht: de kracht van iedereen 230 2.540 3.540 2.090 2.090 Totaal 3.110 18.628 28.403 22.303 22.268 Bedragen zijn in duizenden euro's 4.1 Utrecht: plaats van iedereen Utrecht: plaats van iedereen 2018 2019 2020 2021 2022 Utrechtse Onderwijsagenda 0 650 650 410 400 In stand houden kwaliteit en infrastructuur onderwijs achterstandenbeleid 0 0 2.000 2.200 2.400 Verbeteren en uitbreiden maatschappelijke stages 0 50 50 50 50 Regionaal Investeringsplatform 0 0 3.000 0 0 Investeren in ecosysteem voor starters en groeiers 0 750 750 500 500 Fonds Mismatch Arbeidsmarkt 0 1.000 500 500 500 Omgevingsvisie Binnenstad 200 200 0 0 0 Voortzetten evenementenbeleid 0 440 300 300 300 Vuelta 2020 0 800 0 0 0 Castellum Hoge Woerd (vanaf 2020 in groeikader verwerken) 0 100 0 0 0 Jongerencultuurhuis Overvecht 0 220 200 200 200 Religieus Cultureel Erfgoed 0 0 50 75 75 Armoederegelingen 0 500 500 500 500 Maatschappelijke initiatieven armoedebeleid 0 100 100 100 100 Impuls buurtgerichte vroegsignalering schulden 0 300 400 500 500 Voorkomen van schulden en innoveren schuldhulpverlening voor jongeren en ZZP'ers. 0 300 400 500 0 Pilot huurverlaging 0 500 500 0 0 Bijdrage studenten met een functiebeperking 0 140 140 140 285 Voedselbanken meer zekerheid op langdurig gebruik van lokaties 0 150 150 150 150 Flexibel, snel in te zetten budget tbv acute knelpunten toegankelijkheid, looproutes Solgu 0 275 275 275 275 Utrecht Zijn We Samen: anti discriminatie agenda 0 0 150 150 150 Utrecht Zijn We Samen: tegengaan polarisatie en radicalisering 0 0 250 570 570 Tegengaan laaggeletterdheid, vergroten 0 250 250 250 250 33 digivaardigheden Onderzoek extra zwembad 0 25 0 0 0 Buurtpacten (samenwerking partijen, voorkomen overbelasting mantelzorgers) 0 100 50 0 0 Versterken Sociale Basis Jeugd en JGZ ter voorkoming van wachtlijsten 0 500 500 500 500 Voortzetten en intensiveren aanpak ondermijning 0 250 250 635 635 Voortzetten extra inzet wijk BOA's en Toezicht &amp;amp; Handhaving 's nachts 0 0 550 550 550 Ketenregisseur voorkomen mensenhandel 0 100 100 100 100 Voorkomen misbruik minderjarigen in de seksindustrie, aanbod uitstapprogramma's 0 100 100 100 100 Totaal 200 7.800 12.165 9.255 9.090 Bedragen zijn in duizenden euro's Voor de inhoudelijke toelichting op de hier weergegeven intensiveringen in relatie tot de maatregelen in het coalitieakkoord verwijzen wij naar het eerste hoofdstuk van het coalitieakkoord, Utrecht: plaats voor iedereen. 34 4.2 Utrecht: nieuwe energie van iedereen Utrecht: nieuwe energie van iedereen 2018 2019 2020 2021 2022 Versnellingsaanpak wonen 0 500 500 0 0 Nieuwe woonconcepten 0 508 500 500 500 Aanpak Huisjesmelkers 0 520 520 0 0 Mobiliteit voor iedereen (fietslessen, fiets in U-pas) 50 50 50 50 50 Voortzetten koers SRSRSB, verbinden mobiliteit met binnenstedelijke ontwikkelingen 300 900 2.150 2.150 2.150 Aanpak &lt;b&gt;verkeersveiligheid&lt;/b&gt; 0 0 1.250 1.250 1.250 Schaalsprong mobiliteit (o.a.&lt;br&gt;Project Geautoriseerde uitgaven t/m 2018 conform Programma- Voorgestelde wijziging Actuele autorisatie uitgaven t/m 2018 begroting 2018 Budgettair neutrale aanpassingen aan budget Randstadspoor Fietsparkeervoorzieningen station Overvecht aan de kant van Tuindorp 100 -100 0 Fiets- (sternet) en voetgangersvoorzieningen en kiss and ride strook (OV knooppunt) station Zuilen 500 -500 0 Fiets- (sternet) en voetgangersvoorzieningen (OV knooppunt) station Lunetten 500 -500 0 Verbeteren fietsenstalling bij station Terwijde 100 -100 0 Fietsvoorzieningen RSS overige stations muv Overvecht Noord en Vleuten 0 1.200 1.200 43 Project Geautoriseerde uitgaven t/m 2018 conform Programma- Voorgestelde wijziging Actuele autorisatie uitgaven t/m 2018 begroting 2018 Aanpassingen aan budget Beter Benutten Vervolg De gebruiker Centraal Vervolg 2016-2017 2.001 160 2.161 Fietsimpuls 262 -49 213 Slimme kruisingen 600 177 777 Actieplan Goederenvervoer 4.253 -349 3.904 Integrale aanpak Vondellaan 800 800 1.600 Aanpassingen overige subsidies/bijdragen Hoofdfietsroutes, incl. fiets file vrij en aanvullend 24.970 -189 24.781 Kwaliteit fietsroutes stations 2.500 64 2.564 fietsroute Oosterspoorbaan 1.500 150 1.650 Doorfietsroute om de OostTolsteeg Maliesingel 1.500 100 1.600 Schoolchance 0 251 251 HOV Leidsche Rijn (N40, N50, Z50) 15.113 -6.365 8.748 Busbaan Kruisvaart 11.000 -793 10.207 Budgettair neutraal verschuiven budget tussen projecten Doorfietsroutes 4 Noordelijke Singelring 3.500 -250 3.250 Doorfietsroute om de Oost resterende trac&eacute; 2.309 250 2.559 handhaving Taxikeurmerk (5 jaar) 250 100 350 investeringen tbv taxistandplaatsen 100 -100 0 Autorisaties van doorlopende projecten Knip Maarssenseweg 1.200 300 1.500 Westelijke Stadsboulevard (MUW) 4.700 1.400 6.100 Herprogrammering GU-budget en Verder budet in MPB 2018 Dafne Schippersbrug 23.271 -4.809 18.462 Invoering leenfietsen 4.111 -3.090 1.021 Randstadspoor 11.696 -2.079 9.617 Vervoersplan 2018 en 2019 600 600 Slim regelen 2.000 2.000 Continu&iuml;teit &lt;b&gt;verkeersveiligheid&lt;/b&gt; 1.000 1.000 Actieplan Schoon vervoer 4.757 1.000 5.757 Totaal 121.593 -9.721 111.872 Bedragen zijn in duizenden euro's Aanpassingen in verband met subsidies Randstadspoor Op 11 december 2017 heeft de provincie in het kader van Randstadspoor een subsidie verleend voor de knooppuntontwikkeling Vaartsche Rijn (integrale aanpak Vondellaan) en voor de overige stations.&lt;br&gt;De raad ontvangt tweemaal per jaar de voortgangsrapportage &lt;b&gt;Verkeersveiligheid&lt;/b&gt;, daarin staat de stavaza van de programma &lt;b&gt;verkeersveiligheid&lt;/b&gt;.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt;&lt;li&gt; &lt;span class=&quot;searchResultLabel&quot;&gt; &lt;a href=&quot;/Agenda/Details/Utrecht/ea71c6eb-904a-4de2-bc0c-b81924563230&quot;&gt; &lt;span class=&quot;searchResultKeyword&quot;&gt;Commissie Stad en Ruimte&lt;/span&gt; - &lt;span class=&quot;searchResultDate&quot;&gt;21-06-2018&lt;/span&gt; &lt;/a&gt; &lt;/span&gt; &lt;span class=&quot;searchResultListtype&quot;&gt; &lt;a href=&quot;https://api1.ibabs.eu/publicdownload.aspx?site=Utrecht&amp;amp;id=1b0c9779-3fc3-4a59-afb2-32be96d37882&quot; target=&quot;_blank&quot;&gt;STVV Voorjaarsnota 2018 en 1e Berap 2018.pdf&lt;/a&gt; &lt;/span&gt; &lt;span" + \
		" class=&quot;searchResultText&quot;&gt; &lt;span class=&quot;searchResult&quot;&gt; Intensiveringen 2018 2019 2020 2021 2022 Utrecht: plaats van iedereen 200 7.800 12.165 9.255 9.090 Utrecht: nieuwe energie van iedereen 2.680 8.288 12.698 10.958 11.088 Utrecht: de kracht van iedereen 230 2.540 3.540 2.090 2.090 Totaal 3.110 18.628 28.403 22.303 22.268 Bedragen zijn in duizenden euro's 4.1 Utrecht: plaats van iedereen Utrecht: plaats van iedereen 2018 2019 2020 2021 2022 Utrechtse Onderwijsagenda 0 650 650 410 400 In stand houden kwaliteit en infrastructuur onderwijs achterstandenbeleid 0 0 2.000 2.200 2.400 Verbeteren en uitbreiden maatschappelijke stages 0 50 50 50 50 Regionaal Investeringsplatform 0 0 3.000 0 0 Investeren in ecosysteem voor starters en groeiers 0 750 750 500 500 Fonds Mismatch Arbeidsmarkt 0 1.000 500 500 500 Omgevingsvisie Binnenstad 200 200 0 0 0 Voortzetten evenementenbeleid 0 440 300 300 300 Vuelta 2020 0 800 0 0 0 Castellum Hoge Woerd (vanaf 2020 in groeikader verwerken) 0 100 0 0 0 Jongerencultuurhuis Overvecht 0 220 200 200 200 Religieus Cultureel Erfgoed 0 0 50 75 75 Armoederegelingen 0 500 500 500 500 Maatschappelijke initiatieven armoedebeleid 0 100 100 100 100 Impuls buurtgerichte vroegsignalering schulden 0 300 400 500 500 Voorkomen van schulden en innoveren schuldhulpverlening voor jongeren en ZZP'ers. 0 300 400 500 0 Pilot huurverlaging 0 500 500 0 0 Bijdrage studenten met een functiebeperking 0 140 140 140 285 Voedselbanken meer zekerheid op langdurig gebruik van lokaties 0 150 150 150 150 Flexibel, snel in te zetten budget tbv acute knelpunten toegankelijkheid, looproutes Solgu 0 275 275 275 275 Utrecht Zijn We Samen: anti discriminatie agenda 0 0 150 150 150 Utrecht Zijn We Samen: tegengaan polarisatie en radicalisering 0 0 250 570 570 Tegengaan laaggeletterdheid, vergroten 0 250 250 250 250 33 digivaardigheden Onderzoek extra zwembad 0 25 0 0 0 Buurtpacten (samenwerking partijen, voorkomen overbelasting mantelzorgers) 0 100 50 0 0 Versterken Sociale Basis Jeugd en JGZ ter voorkoming van wachtlijsten 0 500 500 500 500 Voortzetten en intensiveren aanpak ondermijning 0 250 250 635 635 Voortzetten extra inzet wijk BOA's en Toezicht &amp;amp; Handhaving 's nachts 0 0 550 550 550 Ketenregisseur voorkomen mensenhandel 0 100 100 100 100 Voorkomen misbruik minderjarigen in de seksindustrie, aanbod uitstapprogramma's 0 100 100 100 100 Totaal 200 7.800 12.165 9.255 9.090 Bedragen zijn in duizenden euro's Voor de inhoudelijke toelichting op de hier weergegeven intensiveringen in relatie tot de maatregelen in het coalitieakkoord verwijzen wij naar het eerste hoofdstuk van het coalitieakkoord, Utrecht: plaats voor iedereen. 34 4.2 Utrecht: nieuwe energie van iedereen Utrecht: nieuwe energie van iedereen 2018 2019 2020 2021 2022 Versnellingsaanpak wonen 0 500 500 0 0 Nieuwe woonconcepten 0 508 500 500 500 Aanpak Huisjesmelkers 0 520 520 0 0 Mobiliteit voor iedereen (fietslessen, fiets in U-pas) 50 50 50 50 50 Voortzetten koers SRSRSB, verbinden mobiliteit met binnenstedelijke ontwikkelingen 300 900 2.150 2.150 2.150 Aanpak &lt;b&gt;verkeersveiligheid&lt;/b&gt; 0 0 1.250 1.250 1.250 Schaalsprong mobiliteit (o.a.&lt;br&gt;Project Geautoriseerde uitgaven t/m 2018 conform Programma- Voorgestelde wijziging Actuele autorisatie uitgaven t/m 2018 begroting 2018 Budgettair neutrale aanpassingen aan budget Randstadspoor Fietsparkeervoorzieningen station Overvecht aan de kant van Tuindorp 100 -100 0 Fiets- (sternet) en voetgangersvoorzieningen en kiss and ride strook (OV knooppunt) station Zuilen 500 -500 0 Fiets- (sternet) en voetgangersvoorzieningen (OV knooppunt) station Lunetten 500 -500 0 Verbeteren fietsenstalling bij station Terwijde 100 -100 0 Fietsvoorzieningen RSS overige stations muv Overvecht Noord en Vleuten 0 1.200 1.200 43 Project Geautoriseerde uitgaven t/m 2018 conform Programma- Voorgestelde wijziging Actuele autorisatie uitgaven t/m 2018 begroting 2018 Aanpassingen aan budget Beter Benutten Vervolg De gebruiker Centraal Vervolg 2016-2017 2.001 160 2.161 Fietsimpuls 262 -49 213 Slimme kruisingen 600 177 777 Actieplan Goederenvervoer 4.253 -349 3.904 Integrale aanpak Vondellaan 800 800 1.600 Aanpassingen overige subsidies/bijdragen Hoofdfietsroutes, incl. fiets file vrij en aanvullend 24.970 -189 24.781 Kwaliteit fietsroutes stations 2.500 64 2.564 fietsroute Oosterspoorbaan 1.500 150 1.650 Doorfietsroute om de OostTolsteeg Maliesingel 1.500 100 1.600 Schoolchance 0 251 251 HOV Leidsche Rijn (N40, N50, Z50) 15.113 -6.365 8.748 Busbaan Kruisvaart 11.000 -793 10.207 Budgettair neutraal verschuiven budget tussen projecten Doorfietsroutes 4 Noordelijke Singelring 3.500 -250 3.250 Doorfietsroute om de Oost resterende trac&eacute; 2.309 250 2.559 handhaving Taxikeurmerk (5 jaar) 250 100 350 investeringen tbv taxistandplaatsen 100 -100 0 Autorisaties van doorlopende projecten Knip Maarssenseweg 1.200 300 1.500 Westelijke Stadsboulevard (MUW) 4.700 1.400 6.100 Herprogrammering GU-budget en Verder budet in MPB 2018 Dafne Schippersbrug 23.271 -4.809 18.462 Invoering leenfietsen 4.111 -3.090 1.021 Randstadspoor 11.696 -2.079 9.617 Vervoersplan 2018 en 2019 600 600 Slim regelen 2.000 2.000 Continu&iuml;teit &lt;b&gt;verkeersveiligheid&lt;/b&gt; 1.000 1.000 Actieplan Schoon vervoer 4.757 1.000 5.757 Totaal 121.593 -9.721 111.872 Bedragen zijn in duizenden euro's Aanpassingen in verband met subsidies Randstadspoor Op 11 december 2017 heeft de provincie in het kader van Randstadspoor een subsidie verleend voor de knooppuntontwikkeling Vaartsche Rijn (integrale aanpak Vondellaan) en voor de overige stations.&lt;br&gt;De raad ontvangt tweemaal per jaar de voortgangsrapportage &lt;b&gt;Verkeersveiligheid&lt;/b&gt;, daarin staat de stavaza van de programma &lt;b&gt;verkeersveiligheid&lt;/b&gt;.&lt;br&gt; &lt;/span&gt; &lt;/span&gt; &lt;/li&gt; &lt;/ul&gt;"
		quest = "Wat voor zorgen spelen bij de bewoners omtrent verkeersveiligheid?"
		f = 0
		manualqId = 1
	else:
		ord = RandomisationOrder.objects.get(manual_id=sessionId, presentOrder=randomId-2)
		f = ord.searchtype
		print('me')
		print(ord.searchtype)
		res = Result.objects.get(query=ord.question, engine=ord.searchtype).html
		quest = ord.question.question
		manualqId = ord.question.manual_id
	
	results = res.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&amp;", "&").replace("</span>", "</span><br>").replace("<ul", "<ol").replace("</ul>", "</ol>")
	
	#for each combo search engine, question, indicate doctype
	doctypes = ['Debatresultaat', 'Besluit', 'Debatresultaat',
		'Debatresultaat', 'Besluit', 'Informerend', 'Debatresultaat', 'Informerend']
	if f > 0:
		doctype = doctypes[manualqId]
	else:
		doctype = 'all'
	#if f == 1:
	#	docnames = 
	
	context = {
		'sessionId' : sessionId,
		'randomId' : randomId,
		'results' : results,
		'question' : quest,
		'doctype' : doctype,
	}
	return HttpResponse(render(request, 'uiquery/experiment.html', context))

def preparation(request, sessionId):
	context = {
		'sessionId' : sessionId
	}
	return HttpResponse(render(request, 'uiquery/preparation.html', context))

def ci95(a):
	return st.t.interval(0.95, len(a)-1, loc=np.mean(a), scale=st.sem(a))
	
def printResults(answers):
	seconds = []
	selecteds = []
	likerts = []
	for answer in answers:
		if answer.randomisationId != 0:
			likerts.append(answer.likert)
		seconds.append(answer.answeringTimeS)
		selecteds.append(answer.numSelected)
	print('likert')
	print(np.mean(likerts))
	print(ci95(likerts))
	print('likert var')
	print(np.var(likerts))
	print('seconds')
	print(np.mean(seconds))
	print(ci95(seconds))
	print('selecteds')
	print(np.mean(selecteds))
	print(ci95(selecteds))

def printANOVA(answers):
	MOS = []
	for qId in range(0, 8):
		MOS.append(np.mean(answers[qId]))
	return MOS
	
def results(request):
	as0 = []
	as1 = []
	as2 = []
	for order in RandomisationOrder.objects.filter(searchtype=0):
		ans = Answer.objects.filter(randomisationId=order.manual_id, presentedId = order.presentOrder)
		for a in ans:
			as0.append(a)
	for order in RandomisationOrder.objects.filter(searchtype=1):
		ans = Answer.objects.filter(randomisationId=order.manual_id, presentedId = order.presentOrder)
		for a in ans:
			as1.append(a)
	for order in RandomisationOrder.objects.filter(searchtype=2):
		ans = Answer.objects.filter(randomisationId=order.manual_id, presentedId = order.presentOrder)
		for a in ans:
			as2.append(a)

	print('Search engine ALL')
	printResults(as0)
	print('')
	print('Search engine FILTER')
	printResults(as1)
	print('')
	print('Search engine PLACEBO')
	printResults(as2)
	print('\n\n\n')
	
	qs0 = []
	qs1 = []
	qs2 = []
	for i in range(0, 8):
		qs0.append([])
		qs1.append([])
		qs2.append([])
	
	for order in RandomisationOrder.objects.filter(searchtype=0):
		if order.manual_id != 0 and order.manual_id != 3:
			for qId in range(0, 8):
				q = Query.objects.get(manual_id=qId)
				if(order.question == q):
				#			rs = order.objects.filter(question=q)
				#these are all 
					for r in Answer.objects.filter(randomisationId=order.manual_id, presentedId=order.presentOrder):
						qs0[qId].append(r.likert)
	for order in RandomisationOrder.objects.filter(searchtype=1):
		if order.manual_id != 0 and order.manual_id != 3:
			for qId in range(0, 8):
				q = Query.objects.get(manual_id=qId)
				if(order.question == q):
				#			rs = order.objects.filter(question=q)
				#these are all 
					for r in Answer.objects.filter(randomisationId=order.manual_id, presentedId=order.presentOrder):
						qs1[qId].append(r.likert)
	for order in RandomisationOrder.objects.filter(searchtype=2):
		if order.manual_id != 0 and order.manual_id != 3:
			for qId in range(0, 8):
				q = Query.objects.get(manual_id=qId)
				if(order.question == q):
				#			rs = order.objects.filter(question=q)
				#these are all 
					for r in Answer.objects.filter(randomisationId=order.manual_id, presentedId=order.presentOrder):
						qs2[qId].append(r.likert)
	print('search engine ALL')
	mos0=printANOVA(qs0)
	print('')
	print('search engine FILTER')
	mos1=printANOVA(qs1)
	print('')
	print('search engine PLACEBO')
	mos2=printANOVA(qs2)
	print('')
	print('anova')
	print(st.f_oneway(mos0,mos1,mos2)) 

	print('size')
	print(EffectSize(mos0,mos1,mos2))
	
	
	
	#Get average response time per user
	
	#Get the order for each user
#	rndorders = []
	#TODO randomid, do we properly use manual? shoudl we use manual?
	#TODO check the results for 3
	alltimes = [[],[],[],[],[],[],[],[],[]]
	alllikerts = [[],[],[],[],[],[],[],[],[]]
	avgtimes = []
	avglikerts = []
	
	manualids = [0,1,2,5,7,4,14,15,16]
	cnt = 0
	for order in RandomisationOrder.objects.all():
		if order.manual_id in manualids:
			times = []
			likerts = []
			for ans in Answer.objects.filter(randomisationId=order.manual_id):
				times.append(ans.answeringTimeS)
				#print(ans.answeringTimeS)
				likerts.append(ans.likert)
			avgtimes.append(np.mean(times))
			avglikerts.append(np.mean(likerts))
	#		if(len(times) != 0):
			#	print(np.shape(alltimes))
			#	alltimes[cnt] = times
			#	alllikerts[cnt] = likerts
	#			print('times')
	#			print(np.mean(times))
	#			print(times)
	#			avgtimes.append(np.mean(times))
			#	print('')
	#			avglikerts.append(np.mean(likerts))
			cnt+=1
	print('times')
	print(avgtimes)
	print('likerts')
	print(avglikerts)
						
	#		for user in InterviewSession.objects.filter(randomOrder=order):
			#get all of this user's answers
	#			for answer in Answer.objects.filter(randomisationId=order.manual_id, presentedId=order.presentOrder):
	
	return HttpResponse('see serverlogs')

def answer(request, sessionId, randomId):
	try:
		selected = request.POST['selected']
		print(selected)
		selectedTotal = request.POST['selectedTotal']
		print(selectedTotal)
		likert = request.POST['likert']
		print(likert)
		timeSpent = request.POST['timeSpent']
		print(timeSpent)
		
		if randomId > 1:
			a = Answer(randomisationId = sessionId,	presentedId = randomId - 2, binarySelections = request.POST['selected'], numSelected = request.POST['selectedTotal'], likert = request.POST['likert'], answeringTimeS = request.POST['timeSpent'])
			a.save()
		
	except (KeyError):
		print('post not set')
	if(randomId == 25):
		return HttpResponse("Thank you!")
	return experiment(request, sessionId, randomId+1)
		
	#return the next view		
#	context = {
	#	'sessionId' : sessionId,
	#	'randomId' : randomId + 1,
#	}
#	return HttpResponse(render(request, 'uiquery/experiment.html', context))