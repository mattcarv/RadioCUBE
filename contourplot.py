import astropy.io.fits as fits
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
from astropy import units as u
import numpy as np


hdul = fits.open('C:/Users/mathe/Downloads/wise1testprojected.fits')
header = hdul[0].header
data = hdul[0].data
wcs = WCS(hdul[0].header)

hdul2 = fits.open('C:/Users/mathe/Downloads/wise4testprojected-2.fits')
data2 = hdul2[0].data
plt.rcParams.update({'font.size': 18})
plt.rcParams["figure.figsize"] = (10,8)

pixel_scale = proj_plane_pixel_scales(wcs)[0] * u.deg / u.pixel
arcmin = 1 * u.arcmin.to(u.deg)
arcmin_pixel = (arcmin / pixel_scale).value

fig, ax = plt.subplots(subplot_kw={'projection': wcs}, 
                               figsize=(10, 8))

im1 = plt.imshow(np.log10(data), origin='lower', cmap='Greys')
im2 = plt.contour(np.log10(data2), origin='lower', cmap='Reds', vmin=2.3218)
circ_radius = 3.98*u.arcsec
conv_circ = circ_radius.to(u.deg)
circ_pixel = (conv_circ/pixel_scale).value
circle = plt.Circle((55, 44), circ_pixel, color='blue', fill=False, 
                    lw=1, ls='--')
ax.add_patch(circle)
plt.plot([6, 6 + arcmin_pixel], [6, 6], color='black', lw=2)
plt.text(6 + arcmin_pixel / 2, 8, '1 arcmin', color='black',
         ha='center', va='bottom', fontsize=16)
plt.grid(color='black', lw=0.5, alpha=0.5)
plt.text(24, 58, 'Flux (log DN)')

cax1 = fig.add_axes([0.165, 0.95, 0.77, 0.04])
cbar1 = fig.colorbar(im1, cax=cax1, orientation='horizontal', spacing='proportional')
cbar1.ax.tick_params(direction='out', labeltop=True, labelbottom=False, top=True, bottom=False)

cax2 = fig.add_axes([0.96, 0.1, 0.03, 0.8])
cbar2 = fig.colorbar(im2, cax=cax2, pad=0.03)
cbar2.set_label('Flux (log DN)')

ax.annotate("", xy=(26, 22), xytext=(19, 22),
            arrowprops=dict(arrowstyle="->", lw=2, color='red'),
            ha='center', va='center', color='red', fontsize=14)
ax.text(22, 22.5, 'HD279085', color='black', ha='right', va='bottom', fontsize=16)


ax.coords['ra'].set_axislabel('Right Ascension (J2000)')
ax.coords['dec'].set_axislabel('Declination (J2000)')

plt.subplots_adjust(left=0.15,
                    bottom=0.1,
                    right=0.95,
                    top=0.9,
                    wspace=0.6,
                    hspace=0)
plt.show()


#%%
from matplotlib.patches import Rectangle

# Load FITS data
hdul = fits.open('C:/Users/mathe/OneDrive/Documents/GitHub/U2885_files/moment0final.fits')
header = hdul[0].header
data = hdul[0].data
wcs = WCS(header)

plt.rcParams.update({'font.size': 18})
plt.rcParams["figure.figsize"] = (10, 8)

pixel_scale = proj_plane_pixel_scales(wcs)[0] * u.deg / u.pixel
arcmin = 1 * u.arcmin.to(u.deg)
arcmin_pixel = (arcmin / pixel_scale).value

fig, ax = plt.subplots(subplot_kw={'projection': wcs}, figsize=(10, 8))

# Plot the moment map
im1 = plt.imshow(data, origin='lower', cmap='winter')

circ_radius = 22.2*u.arcsec
conv_circ = circ_radius.to(u.deg)
circ_pixel = (conv_circ/pixel_scale).value
circle = plt.Circle((60, 64), circ_pixel, color='red', fill=False, 
                    lw=1, ls='--')
ax.add_patch(circle)
ax.add_patch(Rectangle((1, 49), 68, 25, edgecolor='blue',ls='--', fill=False,
                       angle=-44.97, alpha=0.7))
ax.add_patch(Rectangle((31, 26), 1.2*arcmin_pixel, 0.5*arcmin_pixel,
                       edgecolor='k', ls='--', fill=False,
                       angle=44.97, alpha=0.7, lw=2))


plt.plot([6, 6 + arcmin_pixel], [6, 6], color='black', lw=2)
plt.text(6 + arcmin_pixel / 2, 8, '1 arcmin', color='black', ha='center', va='bottom',
         fontsize=16)
plt.grid(color='black', lw=0.5, alpha=0.3)

cbar1 = fig.colorbar(im1, spacing='proportional')
cbar1.set_label('Integrated Intensity (K km s$^{-1}$)')
#cbar1.set_label('Velocity (km s$^{-1}$)')
#cbar1.set_label('Line Width (km s$^{-1}$)')

ax.coords['ra'].set_axislabel('Right Ascension (J2000)')
ax.coords['dec'].set_axislabel('Declination (J2000)')

plt.show()

#%%
from spectral_cube import SpectralCube

filename = fits.open('maskedcube_final.fits')

cube = SpectralCube.read(filename, format='fits', use_dask=True)

cube = cube.with_spectral_unit(u.km / u.s)

header = filename[0].header
wcs = WCS(filename[0].header)
peak_intensity = cube.max(axis=0)

pixel_scale = proj_plane_pixel_scales(wcs)[0] * u.deg / u.pixel
arcmin = 1 * u.arcmin.to(u.deg)
arcmin_pixel = (arcmin / pixel_scale).value
circ_radius = 22.2*u.arcsec
conv_circ = circ_radius.to(u.deg)
circ_pixel = (conv_circ/pixel_scale).value
circle = plt.Circle((63, 64), circ_pixel, color='red', fill=False, 
                    lw=1, ls='--')


plt.figure(figsize=(10,8))
ax = plt.subplot(projection=peak_intensity.wcs)
ax.add_patch(circle)
ax.grid(True, color='k', lw=0.5, alpha=0.3)
im = ax.imshow(peak_intensity.value, origin='lower', cmap='viridis')
ax.plot([6, 6 + arcmin_pixel], [6, 6], color='black', lw=2)
ax.text(6 + arcmin_pixel / 2, 8, '1 arcmin', color='black',
          ha='center', va='bottom', fontsize=16)
ax.coords['ra'].set_axislabel('Right Ascension (J2000)')
ax.coords['dec'].set_axislabel('Declination (J2000)')
cbar = plt.colorbar(im)
cbar.set_label('Peak (K)')
plt.show()

