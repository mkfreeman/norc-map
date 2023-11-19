# NORC MAP
An interactive map of naturally occuring retirement communities
([NORCs](https://norcinnovationcentre.ca/)) in Toronto and their distances to
the nearest TTC stop. 

## Development
This project was created using the [Vite](https://vitejs.dev/guide/) svelte-ts template. To run the project locally, install
packages with `yarn` and run `yarn dev` (or `npm install` and `npm run dev`).

To deploy the project, run `yarn build` (or `npm run build`).

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