

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
| ID 	| Name		| Domain<sup>1</sup> | Resolution<sup>2</sup> | Features<sup>3</sup> | Duration<sup>4</sup> | Spanned years | Horizons<sup>5</sup>  | Regions<sup>6</sup> | Type<sup>7</sup>|
| -- 	| ------	|------	 | -----------| -----    | -----    | ----------    | -----      | --------------- |----|
|1	| ISO-NE	|S      |60         	|E		|108    |2003-2014     |❌	✔️	✔️	❌      |✔️|📦|
|2	| NYISO		|S	|5		|E		|264	|2001-2023	|✔️	✔️	✔️	❌	|✔️|📦|
|3	| PJM		|S	|60		|E		|240	|1998-2018	|❌	✔️	✔️	✔️	|✔️|📦|
|4	| CIF		|?	|d,m,y		|Undef.		|8-909	|unknown	|❌	❌	✔️	✔️	|❌|📦|
|5	| GEFCOM 14	|S	|60		|E, W, T, PV	|10	|2021		|❌	✔️	❌	❌	|❌|📦|
|6	| EUNITE	|S	|30		|E, T, H	|24	|1997-1999	|❌	✔️	✔️	❌	|❌|📦|
|7	| ENTSO-E	|S	|60		|E		|<=288	|till 2015	|❌	✔️	✔️	✔️	|✔️|📦|
|8	| LCL		|H	|30		|E		|12	|2013		|❌	✔️	❌	❌	|❌|📁|
|9	| SET		|S	|10		|E		|<1	|2013		|✔️	❌	❌	❌	|❌|📁|
|10	| BDG-Proj	|S	|60		|E		|12	|unknown	|❌	✔️	❌	❌	|✔️|📁|
|11	| IHPC		|S	|1		|E		|48	|2006-2010	|✔️	✔️	✔️	✔️	|❌|📁|
|12	| GEFCOM 12	|S	|60		|E, W, T	|42	|2004-2008	|❌	✔️	✔️	❌	|❌|📁|
|13	| OPSD		|S	|15-60		|E, PV, W	|148	|2005-2019	|✔️	✔️	✔️	✔️	|✔️|📁|
|14	| ELD		|S	|15		|E		|36	|2011-2014	|✔️	✔️	✔️	✔️	|❌|📁|
|15	| ENERTALK	|S	|15 hz		|E		|12	|2016		|✔️	✔️	❌	❌	|❌|📁|
|16	| S-TSO		|H	|60		|>25		|24	|2017-2018	|❌	✔️	✔️	❌	|❌|📁|
|17	| RTE-France	|S	|30		|E		|12	|2012-2020	|❌	✔️	❌	❌	|✔️|🌐|
|18	| AEMO		|H	|60		|E		|12	|2013		|❌	✔️	❌	❌	|✔️|🌐|
|19	| IESO-O	|H	|60		|E, P		|20+	|2022-2023	|❌	✔️	✔️	❌	|❌|🌐|
|20	| AESO		|S	|60		|E		|132	|2005-2016	|❌	✔️	✔️	✔️	|❌|🌐|
|21	| PPS		|S	|15-60		|E		|120+	|2013- now	|✔️	✔️	✔️	✔️	|❌|🌐|
|22	| AUSGRID	|S	|15		|E		|204	|2005-2022	|✔️	✔️	✔️	✔️	|✔️|🌐|
|23	| KPX		|H	|5		|E		|240	|2003-now	|✔️	✔️	✔️	✔️	|❌|🌐|
|24	| ADMIE		|S	|60		|E		|120+	|2011-now	|❌	✔️	✔️	✔️	|✔️|🌐|
|25	| Pecan		|S	|15		|E, W		|24	|2017-2018	|✔️	✔️	✔️	❌	|✔️|🌐|


**Legend:**

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
