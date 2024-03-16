<div align="center">

![Python 3.11](https://img.shields.io/badge/Python-3.11-0070CC?logo=python&logoColor=white)
![TOML](https://img.shields.io/badge/TOML-9C4221?logo=toml&logoColor=white)
![LSmall](https://img.shields.io/badge/kB-small-808080)
![Filesize](https://img.badgesize.io/sidstuff/orbital/master/orbital.py.svg)
![CLI](https://img.shields.io/badge/CLI-808080?logo=powershell&logoColor=white)
![Cross Platform](https://img.shields.io/badge/cross–platform-0B4)

</div>

<h1 align="center">Atomic Orbital Scatterplots using Matplotlib [Python] 💡</h1>
<p align="center">Make interactive scatterplots of atomic orbitals and animate them.</p>
<div align="center"><img src="https://github.com/sidstuff/orbital/assets/160637304/9aa275d3-7dea-4bb4-8802-b39607718a20" width="75%"></div>
<div align="center"><pre>python orbital.py 5 3 . 6000 . "both(plt.get_cmap('rainbow'))"</pre></div>

## Dependencies 🔗

* **Matplotlib**
* **NumPy**
* **SymPy**
* **SciPy**
* **FFmpeg** (for MP4 / WebM output)

## Usage `>_`

Download `orbital.py` to a folder and open a terminal there, then enter `python orbital.py` or

On Windows
```cmd
orbital.py
```
On Linux/macOS
```sh
chmod +x orbital.py   # Only the first time
./orbital.py
```
If no arguments are given, the script will ask for the following inputs:
```
n (default 1) =
l (default 0) =
m (default 0) =
Number of dots (default 4000):
Background color (default 'black'):
Change colormap to (optional):
View/Draw/Animate [V/D/A] (default Draw):
```
To choose the default option, simply press `Enter`.

The input for background color will be treated as a string. See ways of specifying color [here](https://matplotlib.org/stable/users/explain/colors/colors.html). Support for (semi-)transparent backgrounds depends on the output format.

The `input()` function for the colormap is enclosed by the `eval()` function, so colormaps can be specified using functions like `pyplot.get_cmap`, `ListedColormap`, and `LinearSegmentedColormap`, imported respectively as `plt.get_cmap`, `lc`, and `lsc`. Visit the following links to see ways of [choosing](https://matplotlib.org/stable/users/explain/colors/colormaps.html) and [creating](https://matplotlib.org/stable/users/explain/colors/colormap-manipulation.html) colormaps.

The color mapping is based on the value of the real wavefunction $\psi$ (psi), with the midpoint of the colormap corresponding to zero. To instead color based on $|\psi|,$ mapping $0$ and $\max(|\psi|)$ to the bottom and top of the colormap respectively, enclose the colormap with `both()`. The default colormap is `'cool'` and `'spring'` concatenated.

<div align="center"><img src="https://github.com/sidstuff/orbital/assets/160637304/dc29385a-6c87-4327-b057-a982e15d74c1" width="75%"></div>
<div align="center"><pre>python orbital.py 3 2 -1</pre></div>

> [!CAUTION]
> Due to the `eval()` function, be careful allowing others to run the script. Enter appropriate values, the script does not attempt to catch errors.

When asked to choose between View, Draw, and Animate, anything that in lowercase does not become `v`, `view`, `d`, or `draw` results in an animation. Choosing View produces an interactive plot. Choosing Draw results in the following prompts:
```
Elevation in degrees (default 0):
Azimuth in degrees (default 0):
Format (default PNG):
```
The supported formats depend on the backend used. The `drawings` folder is created if not already present, and the output is saved to it. If Animate is chosen, the prompts are:
```
Elevation in degrees (default 0):
Initial azimuth in degrees (default 0):
Format [mp4/webm/gif] (default WebM):
Duration in sec (default 12):
```
A video of the orbital rotating 360° degrees within the specified duration, is saved to the `animations` folder.

> [!NOTE]
> The actual duration may be very slightly less, so that the duration times the FPS results in an integer number of frames.

Image and video filenames consist of `(n, l, m)`, the number of dots, and as a suffix, the Unix timastamp in base 36, to avoid similar outputs overwriting each other. The orbital names s, p, d, f, ... are not used, to facilitate regex.

---
Instead of inputting values one by one, you can also supply them as arguments in the same order given above. To choose the default values, use a period. If one or more but not all the values are specified, the remaining will take their default values.

For example,
```
python orbital.py 3 2 . . . "both(plt.get_cmap('plasma'))" a 25
```
refers to a $\mathrm{3d_{z^2}}$ orbital with 4000 dots, a black background, and the `both(plt.get_cmap('plasma'))` colormap. It will produce an animation viewed from an elevation of 25° and initial azimuth of 0°, in the WebM format, lasting 12 s.

<div align="center"><video src="https://github.com/sidstuff/orbital/assets/160637304/37d8ef24-0002-4244-8250-675b4b27cd55"></video></div>

## Advanced Options ⚙️

The options given so far are plenty to play around with and generate beautiful animations in your desired format. To change the defaults, or for further options, create an `override.conf` file in the TOML format containing any of the following keys (in any order) with their desired values.
```toml
n = 1
l = 0
m = 0

dots = 4000
bgcolor = "black"
colormap = "lc(np.vstack((plt.get_cmap('cool')(np.linspace(0,1,256)),plt.get_cmap('spring')(np.linspace(0,1,256)))))"

mode = "draw"

elevation = 0
azimuth = 0   # Also the initial azimuth for animation
format = ["png", "webm"]
duration = 12

resolution = 1080
mp4codec = "libx264"   # Try libx265
webmcodec = "libvpx-vp9"   # Try libsvtav1
fps = 30

dotsize = 32   # In px^2
dotshape = "o"   # See matplotlib.markers
dotalpha = 0.5   # Transparency
```
The default resolution is 1080x1080 so that the output can be displayed without image scaling when fullscreen on a common Full HD (1080p) monitor. The FPS is 30 which seems appropriate for a continuously rotating animation. You may want to increase or decrease these to balance detail and filesize. The GIF format is preferred in some cases, but it uses lossless compression (albeit a severely limited color space), so the relatively high resolution and FPS can lead to a large file size. Modern internet is fast, so these values are not reduced for GIFs by default, but you may want to do so nonetheless.

The newer codecs suggested achieve better compression but much higher encoding and decoding complexity. Ensure that FFmpeg has been built with support for the codec(s) you wish to use. It is also to be noted that unlike MPEG formats, WebM and its associated codecs are free and open, which is why they have been made the defaults.

## Concepts Used 📚

This script uses the Monte Carlo rejection sampling algorithm to generate points according to their probability distribution function (PDF). The three spherical coordinates have separable PDFs, so the three sets can be found independently and then combined.

<div align="center"><img src="https://github.com/sidstuff/orbital/assets/160637304/4e192a42-9f0a-4fd2-b420-b77fbd8b56eb" width="75%"></div>

The algorithm can be inferred from the above image. First we pick a domain for the variable $x,$ and an upper bound on $p(x);$ in the image these are $(-3,3)$ and $0.4167$, respectively. Pairs $x$ and $y$ are randomly generated within the aforemetioned domain and upper bound, respectively. if $y < p(x),\ x$ is kept, otherwise it is discarded. This continues until the desired number of values for $x$ is obtained.

The domains for $\theta$ (theta) and $\phi$ (phi) are of course $0$ to $\pi$ and $-\pi$ to $\pi,$ respectively, but to what distance $r$ should points be plotted? From [Eq. (D.60)](https://web1.eng.famu.fsu.edu/~dommelen/quantum/style_a/nt_rsexp.html), p. 1441, of van Dommelen (2012),[^1] the expectation value of $r$ (in atomic units) for an orbital is given by
$$\langle r\rangle=\frac{3n^2-\ell(\ell+1)}{2}$$

[^1]: van Dommelen, L. (2012). Quantum mechanics for engineers. https://websites.umich.edu/~ners312/CourseLibrary/Dommelen.pdf

I.e., the average distance is $1.5n^2$ for an s orbital and decreases with $\ell$. All orbitals within the same shell $n$ shall be plotted to the same distance, say $1.75\times 1.5n^2=2.625n^2,$ to facilitate comparison. To see where $2.625n^2$ lies w.r.t. each orbital, observe the blue line in this interactive Desmos [graph](https://www.desmos.com/calculator/zze7nelesn).

The same graph also shows that the maximum value of the radial probability $r^2(R(r))^2$ doesn't vary much within a shell $n,$ and is greatest for $\ell=n-1,$ occurring at $x=n^2$ (the green line in the graph). This is because the associated Laguerre polynomial $L_{n-\ell-1}^{2\ell+1}$ in $R(r)$ reduces to $L_0=1,$ leaving only the $r^l$ and $e^{-r/n},$ making it easy to differentiate $r^2(R(r))^2$ and find the location of the peak.

It is common, especially in chemistry, to use real atomic orbitals, which arise from simple linear combinations of complex orbitals. Their azimuthal probability is $\sin^2(m\phi)$ if $m<0$, and $\cos^2(m\phi)$ otherwise, so the maximum here is always $1$.

The polar probability is $(\sin\theta)(P_\ell^m(\cos\theta))^2$ where $P_\ell^m$ is the associated Legendre polynomial. $P_\ell^{-m}\propto P_\ell^m$, so we can replace the latter with $P_\ell^{|m|}$ and only worry about polynomials with $m\geq0$. If $m=\ell,$
$$P_\ell^\ell(\cos\theta)=(-1)^\ell(2\ell-1)!!\sin^\ell(\theta)$$
$$\implies(\sin\theta)(P_\ell^\ell(\cos\theta))^2=((2\ell-1)!!)^2\sin^{2\ell+1}(\theta))$$
<p align="center">where the double factorial</p>

$$(2\ell-1)!!=(2l-1)\cdot(2l-3)\ldots5\cdot3\cdot1=\frac{(2\ell)!}{\ell!\ 2^\ell}$$
The maximum here is clearly $((2\ell-1)!!)^2$, as demonstrated [here](https://www.desmos.com/calculator/hvtjt1hvkc) – the ratio of the polar probability $F$ to the maximum $G$, remains at or below $1$.

For $m=0$, the Bernstein-type inequality[^2][^3]
$$(\sin\theta)(P_\ell^0(\cos\theta))^2<\frac{2}{\pi(\ell+\frac{1}{2})}$$
is similarly demonstrated [here](https://www.desmos.com/calculator/kccvaxhqr4).

[^2]: Antonov, V. A., & Holsevnikov, K. V. (1981). An estimate of the remainder in the expansion of the generating function for the Legendre polynomials (generalization and improvement of Bernstein's inequality). Vestnik Leningrad. Univ. Mat. 13, 163–166.

[^3]: Lorch, L. (1983). Alternative proof of a sharpened form of Bernstein's inequality for Legendre polynomials, Appl. Anal. 14, 237–240.

From Eq. (23), p. 183, of Lohöfer (1998),[^4]
$$(\sin\theta)(P_\ell^m(\cos\theta))^2<\frac{\sqrt{\frac{1.11(2^5)}{\pi^3}(m+1)}}{\ell+\frac{1}{2}}\frac{(\ell+m)!}{(\ell-m)!}$$
But for $m,\ell$ not covered by the previous two cases, i.e., $\ell\geq2,\ 1\leq m\leq\ell-1,$ it [seems](https://www.desmos.com/calculator/hcq2laycjm) a simpler and smaller value suffices:
$$(\sin\theta)(P_\ell^m(\cos\theta))^2<\frac{\sqrt{m+1}}{2\ell+1}\frac{(\ell+m)!}{(\ell-m)!}$$

[^4]: Lohöfer, G. (1998). Inequalities for the associated Legendre functions. J. Approx. Theory, 95 (2), 178–193. https://doi.org/10.1006/jath.1998.3207

Thus we have obtained all the bounds we need to proceed with rejection sampling.

<div align="center"><img src="https://github.com/sidstuff/orbital/assets/160637304/4e6f31df-bef2-42e6-8af5-1904354f3937" width="75%"></div>
<div align="center"><pre>python orbital.py 4 2 . 6000 . "both(plt.get_cmap('gist_earth'))"</pre></div>

### References 📄
