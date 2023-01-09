# Linux commands first
# > module load ants
# Tim Andrews, Jan 2023.

import ants
import ants.fileformats.ancil.preprocessing
import iris
import cftime
import numpy as np
import cf_units

bcs=['holo','lgm','2x']
ancs=['sst','ice']
for bc in bcs:
 for var in ancs:
  # Load in a working RFMIP GC3.1 ancs to get attributes from and use as target grid
  if var == 'sst':
   f1='sst_piControl18501899clim_n96e.anc'
  if var == 'ice':
   f1='ice_piControl18501899clim_n96e.anc'
  anc_existing=ants.load_cube(f1)
  anc_existing=anc_existing[0]

  # Load in new data, overide time-coordinate to be a 360 day calender as required for HadGEM
  # with monthly-mean on day 16 at 00:00:00.
  if var == 'sst':
   fn=bc+'_sst_bc.nc'
   anc_new=ants.load_cube(fn,'sst')
  if var == 'ice':
   fn=bc+'_ice_bc.nc'
   anc_new=ants.load_cube(fn,'ice')
  t = anc_new.coord('time')
  t.units # shows Unit('hours since 2001-01-16 12:00:00', calendar='proleptic_gregorian')
  dtime = t.units.num2date(t.points)
  for i in np.arange(len(dtime)):
   dtime[i]= cftime.DatetimeGregorian(dtime[i].year, dtime[i].month, 16)
  t.points = cftime.date2num(dtime, t.units.origin, calendar=t.units.calendar)
  t.points # shows the first element is -12 which is correct as changed it to 00:00 hour, from 12:00.
           # but then it increments to 732, 1404, 2148..., which we need to be continuous, i.e. 30 day
           # x 24 hr = 720 hour increments from first element.
  xxx=t.points.copy() # t.points elements are read only, so make a copy, change then point t.points to this
  for i in np.arange(len(xxx)):
   xxx[i]=-12.+i*720.
  t.points=xxx
  t.units=cf_units.Unit(t.units.origin, calendar='360_day') # convert to 360 day
  i = anc_new.coord_dims("time")[0]
  anc_new.remove_coord("time")
  anc_new.add_dim_coord(t, i)
  if var == 'ice':
   i=np.where(anc_new.data >= 100.0)
   anc_new.data[i]=100
   i=np.where(anc_new.data <= 0.0)
   anc_new.data[i]=0
   anc_new=anc_new/100. # convert % to fraction
  ants.utils.coord.guess_bounds(anc_new.coord('time')) # add time bounds
  # Set the coordinate system to be the same as anc_existing since we do not have
  # any other information.
  coord_sys=anc_existing.coord("latitude").coord_system
  anc_new.coord("latitude").coord_system=coord_sys
  anc_new.coord("longitude").coord_system=coord_sys
  # Linear regrid of data to target grid
  anc_new=anc_new.regrid(anc_existing,iris.analysis.Linear())  
  # Give new SSTs same attributes as ones we know that work (e.g. stash code etc.)
  anc_new.attributes=anc_existing.attributes
  # Write out new ancil
  ants.fileformats.save(anc_new,bc+'_'+var+'.anc',saver="ancil")
