

![A simle header image](Images/Header1.PNG)


# Publicly Available Datasets For Electric Load Forecasting
A (hopefully eventually) complete listing of the most popular electric LF datasets

### Why?
We found it difficult to find suitable datasets in the flood of information. 
So we came up with the idea of doing a proper search and making the results available to the public.


### What?
Based on a sample set of representative publications, relevant, publicly accessible data sets were extracted, structured and analyzed. 
The details of the search can be found in the scientific publication: `Placeholder - paper is in review right now`


### Improvements? 🤝
We are happy about any kind of cooperation, feedback or extension to make the list even more valuable for other scientists. 
So feel free to expand the list and initiate a pull request.

# The list
| ID  | Abbrev	| Name	                                        | Domain<sup>1</sup> | Resolution<sup>2</sup> | Features<sup>3</sup> | Duration<sup>4</sup> | Spanned years                | Horizons<sup>5</sup>  | Regions<sup>6</sup> | Type<sup>7</sup>|Links|
| -- 	|--       |----------------------------------------------	|------	             | -----------            | -----------          | -----                | --------------------------------------  | -----------------------            | ------------- |----|--------|
|1	| ISO-NE	  |	New England Independent System Operator       |S      |60         	|E		|108    |2003-2014     |❌✔️✔️❌     |✔️|📦|[🔗Link](https://www.iso-ne.com/isoexpress/web/reports/pricing/-/tree/zone-info)|
|2	|NYISO		  | New York Independent System Operator	        |S	|5		|E		|264	|2001-2023	|✔️✔️✔️❌|✔️|📦|[🔗Link](http://mis.nyiso.com/public/P-58Blist.htm)|
|3	|PJM		    | PJM Hourly Energy Consumption                 |S	|60		|E		|240	|1998-2018	|❌✔️✔️✔️|✔️|📦|[🔗Link](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption?resource=download)|
|4	|CIF		    | CIF 2016 competition dataset          	       |?	|d,m,y		|Undef.		|8-909	|unknown	|❌❌✔️✔️|❌|📦|[🔗Link](https://irafm.osu.cz/cif2015/main.php?c=Static&page=download)|
|5	|GEFCOM14  | GEFCom 2014                                  	|S	|60		|E, W, T, PV	|10	|2021		|❌✔️❌❌|❌|📦|[🔗Link](https://www.dropbox.com/s/pqenrr2mcvl0hk9/GEFCom2014.zip?dl=0&file_subpath=%2FGEFCom2014+Data)|
|6	|EUNITE	    | EUNITE 2001                          	        |S	|30		|E, T, H	|24	|1997-1999	|❌✔️✔️❌|❌|📦|[🔗Link](https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/regression.html)|
|7	|ENTSO-E	  | ENTSO-E electric load dataset	                |S	|60		|E		|<=288	|till 2015	|❌✔️✔️✔️|✔️|📦|[🔗Link](https://www.entsoe.eu/publications/statistics-and-data/)|
|8	|LCL		    | LCL Load Dataset (London Households)          |H	|30		|E		|12	|2013		|❌✔️❌❌|❌|📁|[🔗Link](https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households)|
|9	|SET		    | Energy Consumption Dataset for Milano/Trento 	|S	|10		|E		|<1	|2013		|✔️❌❌❌	|❌|📁|[🔗Link](https://www.nature.com/articles/sdata201555)|
|10	|BDG-Proj	  | Building Data Genome Project	                |S	|60		|E		|12	|unknown	|❌✔️❌❌	|✔️|📁|[🔗Link](https://github.com/buds-lab/the-building-data-genome-project)|
|11	|IHPC		    | Individual Household power consumption |S	|1		|E		|48	|2006-2010	|✔️✔️✔️✔️	|❌|📁|[🔗Link](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption)|
|12	|GEFCOM12	| GEFCom 2012	|S	|60		|E, W, T	|42	|2004-2008	|❌✔️✔️❌	|❌|📁|[🔗Link](https://www.kaggle.com/c/global-energy-forecasting-competition-2012-load-forecasting/)|
|13	|OPSD		    | Open Power System Data 	|S	|15-60		|E, PV, W	|148	|2005-2019	|✔️✔️✔️✔️	|✔️|📁|[🔗Link](https://doi.org/10.25832/time_series/2019-06-05)|
|14	|ELD		    | ElectricityLoadDiagrams20112014	|S	|15		|E		|36	|2011-2014	|✔️✔️✔️✔️	|❌|📁|[🔗Link1](https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014) [🔗Link2](https://doi.org/10.24432/C58C86)|
|15	|ENERTALK	  | ENERTALK Dataset Korea (household)	|S	|15 hz		|E		|12	|2016		|✔️✔️❌❌	|❌|📁|[🔗Link](https://www.nature.com/articles/s41597-019-0212-5)|
|16	|S-TSO	    | Spanish Transmission Service operator (TSO)		|H	|60		|>25		|24	|2017-2018	|❌✔️✔️❌	|❌|📁|[🔗Link](https://www.kaggle.com/datasets/nicholasjhana/energy-consumption-generation-prices-and-weather)|
|17	|RTE-France	| RTE France |S	|30		|E		|12	|2012-2020	|❌✔️❌❌	|✔️|🌐|[🔗Link](https://www.rte-france.com/en/eco2mix/download-indicators)|
|18	|AEMO		    | Australian Energy market operator 	|H	|60		|E		|12	|2013		|❌✔️❌❌|✔️|🌐|[🔗Link](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/network-data)|
|19	|IESO-O	    |	IESO Ontario |H	|60		|E, P		|20+	|2022-2023	|❌✔️✔️❌	|❌|🌐|[🔗Link](https://www.ieso.ca/en/Power-Data/Data-Directory)|
|20	|AESO		    | Alberta Electric Sys. Op. Electrical Load Dataset  	|S	|60		|E		|132	|2005-2016	|❌✔️✔️✔️|❌|🌐|[🔗Link](https://www.aeso.ca/market/market-and-system-reporting/data-requests/)|
|21	|PPS		    | Polish power system	|S	|15-60		|E		|120+	|2013- now	|✔️✔️✔️✔️	|❌|🌐|[🔗Link](https://www.pse.pl/web/pse-eng/data/polish-power-system-operation/load-of-polish-power-system)|
|22	|AUSGRID	  | Ausgrid: Distribution zone substation 	|S	|15		|E		|204	|2005-2022	|✔️✔️✔️✔️|✔️|🌐|[🔗Link](https://www.ausgrid.com.au/Industry/Our-Research/Data-to-share/Distribution-zone-substation-data)|
|23	|KPX		    | KPX  Korea	|H	|5		|E		|240	|2003-now	|✔️✔️✔️✔️|❌|🌐|[🔗Link](https://epsis.kpx.or.kr/epsisnew/selectEkgeEpsMepRealChart.do?menuId=030300)|
|24	|ADMIE		  | Independent Electricity Transmission Operator 	|S	|60		|E		|120+	|2011-now	|❌✔️✔️✔️|✔️|🌐|[🔗Link](https://www.admie.gr/en/market/market-statistics/detail-data)|
|25	|Pecan		  | Pecan Street dataset	|S	|15		|E, W		|24	|2017-2018	|✔️✔️✔️❌|✔️|🌐|[🔗Link](https://dataport.pecanstreet.org/)|


#### Legend

<sup>1</sup>Domain: Either system level load (S) or residential load (R)

<sup>2</sup>Resolution: In minutes, if not other stated (d=day, m=month, y=year, hz=1sec)

<sup>3</sup>Features: Electricity (E), Weather (W), Temperature (T), Photovoltaic production (PV), Holiday features (H), Price (P)

<sup>4</sup>Duration: in number of months

<sup>5</sup>Forecasting-Horizons for modelling applicable: Very Short Term (VST), Short Term (ST), Medium Long Term (MT), Long Term (LT)

<sup>6</sup>Dataset records multiple regions separately (e.g. buildings, cities, countries)

<sup>7</sup>Type: Either 📦 = a collection (accumulation of datasets), 📁=a file or achive or 🌐=an data platform / API


*for further details take a look at the publication below ⤵️*



# How to cite
If this work has helped you with your scientific work, we would appreciate a proper mention. ❤️

Our citation recommendation is:
```
The paper is currently in review. We'll update this in a while.
```


# Acknowledgements

💰 We'd like to thank the German Federal Ministry of Economic Affairs and Climate Action (**BMWK**) and the project supervision of the Project Management Jülich (**PtJ**) for the project „FlexGUIde“ which allowed for the work. 

💡 We would also like to thank an **anonymous reviewer** who gave us the idea of publishing the datasets not only in the above-mentioned publication, but also as a repository.
