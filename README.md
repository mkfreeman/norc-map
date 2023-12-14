# NORC MAP
An interactive map of naturally occuring retirement communities
([NORCs](https://norcinnovationcentre.ca/)) in Toronto and their distances to
the nearest TTC stop. 

## Development
This project was created using the [Vite](https://vitejs.dev/guide/) svelte-ts template. To run the project locally, install
packages with `yarn` and run `yarn dev` (or `npm install` and `npm run dev`).

To deploy the project, run `yarn build` (or `npm run build`).

## TTC Stop Amenities
TTC stop amenities, ie benches and shelters, were taken from 3 sources. In all cases, this data was joined with [TTC stop data](https://open.toronto.ca/dataset/ttc-routes-and-schedules/) using the TTC stop_code.
- [Street Furniture - Bench - City of Toronto Open Data Portal](https://open.toronto.ca/dataset/street-furniture-bench/). This data was joined using SITEID column, with the prefix letter 'T' removed. If a stop was found in this dataset, we marked has_bench=True for that stop
- [Street Furniture - Transit Shelter - City of Toronto Open Data Portal](https://open.toronto.ca/dataset/street-furniture-transit-shelter/). This data was joined using SITEID column, with the prefix letter 'T' removed. If a stop was found in this dataset, we marked has_shelter=True for that stop
- A City data set obtained by OpenLab specifically highlighting shelters with benches. This data was joined using "TTC Stop ID." Link here if we can. If a stop was found in this dataset, we marked has_shelter_with_bench=True for that stop

Unforunately, there are a number of issues with this data. As noted on the Open Data Portal, the first two data sets have no description of their columns, and so it is difficult to understand what kind of shelter or bench is present. We made minimal assumptions and hence made the decision noted with each data set above. 

Furthermore, these data sets are inconsistent. Consider the definitions above and see this information:

![image](https://github.com/mkfreeman/norc-map/assets/110122/157fb011-1067-4462-ab26-59776354da2a)

It does not make sense, for example, that has_shelter_with_bench is true for 48 TTC stops where those same stops are marked has_shelter=false based on the other dataset. 

This is noted in more detail here: https://github.com/mkfreeman/norc-map/issues/28#issuecomment-1850468479. Furthermore, at times the datasets do not actually reflect what is shown on Google Streetview (which, we acknowledge, may be out of date, or the dataset could be out of date). 

Based on examination of the data we had, we made a simple rule noted in the issue above which is visible in our interface:

Amenity = "Shelter with Bench Underneath" if has_shelter_with_bench = true

Amenity = "Shelter without bench" if has_shelter_with_bench = false AND has_shelter = true

Amenity = "Bench only" if has_bench = true but the other two are false

This is not perfect, but it conservatively reflects what we can reliably say given the data, without analyzing every single stop on Google StreetView or in person. 


## References / notes
- Leaflet implementation based on [this
  repo](https://github.com/ShipBit/sveltekit-leaflet/), referenced in this
  (actually informative) [video](https://www.youtube.com/watch?v=JFctWXEzFZw&ab_channel=ShipBit)
- Turns out configuring TailwindCSS with Svelte is a bit of a pain, used
  [svelte-add](https://github.com/svelte-add/svelte-add) to do this: `npx --yes
  svelte-add@latest tailwindcss`
- Stops downloaded from [here](https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/7795b45e-e65a-4465-81fc-c36b9dfff169/resource/cfb6b2b8-6191-41e3-bda1-b175c51148cb/download/opendata_ttc_schedules.zip)
- TTC logo downloaded [here](https://worldvectorlogo.com/downloaded/g-03-a101-ttc-logo)
- Building logo downloaded
  [here](https://www.reshot.com/free-svg-icons/item/apartments-5XB6RL3VT7/)
- Route logo downloaded [here](https://www.reshot.com/free-svg-icons/item/map-route-NSD39WHTAV/)
_information below is from the original development set up template_
