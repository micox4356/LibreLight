

import moderngl_window as mglw
import moderngl
#import moderngl.window
import time
#print(dir(moderngl))

#export DISPLAY=:99.0
#Xvfb :99 -screen 0 640x480x24 &
#redirects screen output to invisibel framebuffer 
# python3 main.py --window glfw --fullscreen --samples 16 --cursor false --size 800x600

vertex_shader = """
#version 400

in vec3 in_position;

void main(){
    gl_Position = vec4(in_position, 1);
}
"""

fragment_shaderX = """
#version 400

precision highp float;

uniform float time = 0;
uniform vec2 mouse = vec2(0,0); 
uniform vec2 resolution;


out vec4 fragColor;


float random(float seed)
{
	return fract(sin(seed)*1e4);
}


float row(float x, float y, float row_idx)
{
	float rand_factor = 0.25+random(row_idx)*0.75;
	return step(0.2, y) * step(y, 0.8) * step(0.5, random(floor(x*rand_factor*2. + 15.*time*random(rand_factor))));
}

void main()
{
	vec2 uv = gl_FragCoord.xy / resolution.y;
	uv.x *= 10.0;
	uv.y *= 35.0;
	
	float c = row(uv.x, fract(uv.y), floor(uv.y));
	
	fragColor = vec4(c);
}
"""

#matrix like
fragment_shaderX = """
#version 400
#extension GL_OES_standard_derivatives : enable

precision highp float;
out vec4 fragColor;

uniform float time;
uniform vec2 mouse;
uniform vec2 resolution;

float random(float seed)
{
	return fract(sin(seed)*40002 );//*200e2);
}


float row(float x, float y, float row_idx)
{
	float rand_factor1 = 0.15+random(row_idx)*0.75;
	float rand_factor2 = 0.15+random(row_idx/2.1)*0.75;
	return step(0.3, y) * step(y, 0.7) * step(0.4, random(floor(x*rand_factor1*-3.0 + 30.100*time*random(rand_factor2))));
}

void main()
{
	vec2 uv = gl_FragCoord.yx / resolution.y;
	uv.x *= 20.5;
	uv.y *= 120.0;
	
	float c = row(uv.x, fract(uv.y), floor(uv.y));
	
	fragColor = vec4(c);
}

"""

# shadow bar
fragment_shaderX = """
#version 400
//https://glslsandbox.com/e#97695.0

#extension GL_OES_standard_derivatives : enable
out vec4 fragColor;

precision highp float;

uniform float time;
uniform vec2 mouse;
uniform vec2 resolution;

void main( void ) {

	vec2 pos = ( gl_FragCoord.xy / resolution.xy );

        float color = 0.0;//sin(6.28*0.5*(time-pos.x))*0.5+sin(6.28*1.0*(time+pos.x/0.5))*0.5;

	for(float i=0.0;i<10.0;i+=1.0){
	  color += sin(6.28*0.3*i*(time*i*0.05-pos.x/1.0))*0.03+sin(6.28*1.0*i*(time*i*0.01-pos.x/0.7)+i*2.0)*0.03;
	  color += sin(6.28*0.3*i*(time*i*0.05+pos.x/1.2))*0.03+sin(6.28*1.0*i*(time*i*0.01+pos.x/0.5)+i*0.7)*0.03;
	}


	color *= sin(3.14*pos.x);


	fragColor = vec4( vec3( color*2, color*2,color*2 ), 1.0 );

}
"""


#waves
fragment_shaderX = """
#version 400
//#extension GL_OES_standard_derivatives : enable
//https://glslsandbox.com/e#97629.0
out vec4 fragColor;

#ifdef GL_ES
precision highp float;
#endif

//#extension GL_OES_standard_derivatives : enable

uniform float time;
uniform vec2 resolution;


void main( void ) {
	vec2 uv = (gl_FragCoord.xy - resolution * 0.7) / max(resolution.x, resolution.y) * 3.0;
	uv *= 3.0;

	float e = 0.0;
	for (float i=3.0;i<=5.0;i+=1.0) {
		e += 0.007/abs( (i/15.) +sin((time/9.0) + 0.15*i*(uv.x) *( cos(i/4.9 + (time / 9.0) + uv.x*1.2) ) ) + 3.5*uv.y);
        fragColor = vec4( vec3(e/39.1, e/0.6, e/3.6), 9.0);

	}

}
"""

# sea 
fragment_shaderX = """
#version 400
//#extension GL_OES_standard_derivatives : enable
out vec4 fragColor;

precision highp float;

uniform float time;
uniform vec2 mouse;
uniform vec2 resolution;

float spike(float x) {
	x = mod(x, 2.0);
	
	if (x < 1.0)
		return x * x;
	
	x = 2.0 - x;
	
	return x * x;
}


float noise(float x, float amplitude) {
	float n = spike(x*3.0 + time) * 0.03 +
		sin(x*30.5 + time*26.5) * 0.005 + 
		sin(time) * 0.1;
	return n * amplitude;
}

const vec3 sky_high = vec3(92, 176, 255) / 255.0;
const vec3 sky_low = vec3(219, 238, 255) / 255.0;
const vec3 water = vec3(62, 153, 180) / 255.0;

float fog = 6.0;

void main() {

	vec2 uv = (gl_FragCoord.xy / resolution.xy);

	float v = 0.0;

	float n0 = noise(uv.x * 3.18, 0.3);
	float n1 = noise(uv.x * 2.34, 0.4);
	float n2 = noise(uv.x * 2.14, 0.6);
	float n3 = noise(uv.x * 1.4, 0.8);
	float n4 = noise(uv.x * 1.23, 1.0);
	
	if (uv.y < 0.2 + n4) {
		v = 1.2;
	} else if (uv.y < 0.3 + n3) {
		v = 1.4;
	} else if (uv.y < 0.35 + n2) {
		v = 1.6;
	} else if (uv.y < 0.385 + n1) {
		v = 1.8;
	} else if (uv.y < 0.4 + n0) {
		v = 2.6;
	}

	   
	vec3 color = mix(sky_low, sky_high, uv.y);

	if (v > 0.0) {
		vec3 water_color = water * v;
		//color = water_color;
		color = mix(mix(sky_high, sky_low, 0.5), water_color, clamp(2.0-(uv.y*uv.y*uv.y)*fog, 3.3, 2.6));
		
	}
	
	fragColor = vec4(color, 5.0);
}
"""


#flow
fragment_shaderX = """
#version 400
out vec4 fragColor;
//#extension GL_OES_standard_derivatives : enable
//https://glslsandbox.com/e#97672.0

precision highp float;

uniform float time;
const float ZOOM = 80.0;
const float SPEED = 0.20;

void main( void ) {
	
	vec2 pos = gl_FragCoord.xy / ZOOM;
	float dist;
	float dist1;
	
	for(int i = 0; i < 20; i++) {
		dist = distance(pos.x, pos.y);
        dist = 0.5;
        //dist = rand(vec2(0.1,0.4));
        //dist = hash(1);
        //dist = rand2(vec2(1,10));
        //dist = nois(0.456);
        //dist1 = hash(10);
		
		pos.x = pos.x + sin(time / SPEED) + cos(pos.y + sin(dist));
		pos.y = pos.y - cos(time / SPEED) + sin(pos.x - sin(dist));	
	}

	fragColor = vec4( 0,0,sin(pos.x /10),  1.0);

}
"""


# dimming grid 
fragment_shaderX = """
#version 400
out vec4 fragColor;

//#extension GL_OES_standard_derivatives : enable

precision highp float;

uniform float time;
uniform vec2 mouse;
uniform vec2 resolution;

#define step 100.0
#define width 2.0

#define bigval 0.8
#define smallval 0.4
#define bgval 0.2

float h21(vec2 p)
{
	p = fract(p * vec2(123.34, 456.21));
	p += dot(p, p+45.32);
	return fract(p.x*p.y);
}

void main(void)
{
	vec2 pos = gl_FragCoord.xy - mouse.xy * resolution.xy;
	vec2 lpos = mod(pos, step);
	vec2 id = floor(pos / step);

	float lbg = mod(h21(id), bgval);
	float val = (sin((lbg + 1.0) * time) * bgval + bgval) * 0.5;
	if (lpos.x < width)
	{
		if (abs(mod(id.x, 5.0)) < 0.5)
			val = bigval;
		else
			val = smallval;
	}
	if (val < bigval)
	{
		if (lpos.y < width)
		{
			if (abs(mod(id.y, 5.0)) < 0.5)
				val = bigval;
			else
				val = smallval;
		}
	}
	gl_FragColor = vec4(0,0,val, 1.0);

}
"""


fragment_shader = """
#version 400
out vec4 fragColor;

// https://glslsandbox.com/e#97668.0


#ifdef GL_ES
precision highp float;
#endif

// ↙
//  ↙
//   ↙
// http://66.media.tumblr.com/2a2f183dc4a6a040ff65355418b9403/tumblr_ncbj5rJvLI1tmxmpzo1_500.jpg

vec2 uv;

uniform float time;
uniform vec2 resolution;

const vec2 ch_size  = vec2(1.0, 2.0) * 0.6;              // character size (Y,X)
const vec2 ch_space = ch_size + vec2(1.0, 1.0);    // character distance Vector(X,Y)
const vec2 ch_start = vec2 (ch_space.x * -1.75, 3.25); // start position
      vec2 ch_pos   = vec2 (0.0, 0.0);             // character position(X,Y)
//      vec3 ch_color = vec3 (1.5, 0.75, 0.5);        // character color (R,G,B)
//const vec3 bg_color = vec3 (0.2, 0.2, 0.2);        // background color (R,G,B)

#define REPEAT_SIGN false // True/False; True=Multiple, False=Single

/* 16 segment display...Akin to LED Display.

Segment bit positions:
  __2__ __14__
 |\    |    /|
 | \   |   / |
 5  11 40 9  0
 |   \ | /   |
 |    \|/    |
  _12__ __8__
 |           |
 |    /|\    |
 4   / | \   7
 | 13 1  15 |
 | /   |   \ |
  __3__|__6__

15 12 11 8 7  4 3  0
 |  | |  | |  | |  |
 0000 0000 0000 0000
10101010101010101011

example: letter A

   12    8 7  4 3210
    |    | |  | ||||
 0001 0001 1001 1111

 binary to hex -> 0x119F
*/

#define n0 ddigit(0x22FF);
#define n1 ddigit(0x0281);
#define n2 ddigit(0x1177);
#define n3 ddigit(0x11E7);
#define n4 ddigit(0x5508);
#define n5 ddigit(0x11EE);
#define n6 ddigit(0x11FE);
#define n7 ddigit(0x2206);
#define n8 ddigit(0x11FF);
#define n9 ddigit(0x11EF);

#define A ddigit(0x119F);
#define B ddigit(0x927E);
#define C ddigit(0x007E);
#define D ddigit(0x44E7);
#define E ddigit(0x107E);
#define F ddigit(0x101E);
#define G ddigit(0x807E);
#define H ddigit(0x1199);
#define I ddigit(0x4466);
#define J ddigit(0x4436);
#define K ddigit(0x9218);
#define L ddigit(0x0078);
#define M ddigit(0x0A99);
#define N ddigit(0x8899);
#define O ddigit(0x00FF);
#define P ddigit(0x111F);
#define Q ddigit(0x80FF);
#define R ddigit(0x911F);
#define S ddigit(0x8866);
#define T ddigit(0x4406);
#define U ddigit(0x00F9);
#define V ddigit(0x2218);
#define W ddigit(0xA099);
#define X ddigit(0xAA00);
#define Y ddigit(0x4A00);
#define Z ddigit(0x2266);
#define _ ch_pos.x += ch_space.x;
#define s_dot     ddigit(0);
#define s_minus   ddigit(0x1100);
#define s_plus    ddigit(0x5500);
#define s_greater ddigit(0x2800);
#define s_less    ddigit(0x8200);
#define s_sqrt    ddigit(0x0C02);
#define nl1 ch_pos = ch_start;  ch_pos.y -= 3.0;
#define nl2 ch_pos = ch_start;  ch_pos.y -= 6.0;
#define nl3 ch_pos = ch_start;	ch_pos.y -= 9.0;
#define nl4 ch_pos = ch_start;	ch_pos.y -= 12.0;

float dseg(vec2 p0, vec2 p1)
{
	vec2 dir = normalize(p1 - p0);
	vec2 cp = (uv - ch_pos - p0) * mat2(dir.x, dir.y,-dir.y, dir.x);
	return distance(cp, clamp(cp, vec2(0), vec2(distance(p0, p1), 0)));
}

bool bit(int n, int b)
{
	return mod(floor(float(n) / exp2(floor(float(b)))), 2.0) != 0.0;
}

float d = 1e6;

void ddigit(int n)
{
	float v = 1e6;
	vec2 cp = uv - ch_pos;
	if (n == 0)     v = min(v, dseg(vec2(-0.405, -1.000), vec2(-0.500, -1.000)));
	if (bit(n,  0)) v = min(v, dseg(vec2( 0.500,  0.063), vec2( 0.500,  0.937)));
	if (bit(n,  1)) v = min(v, dseg(vec2( 0.438,  1.000), vec2( 0.063,  1.000)));
	if (bit(n,  2)) v = min(v, dseg(vec2(-0.063,  1.000), vec2(-0.438,  1.000)));
	if (bit(n,  3)) v = min(v, dseg(vec2(-0.500,  0.937), vec2(-0.500,  0.062)));
	if (bit(n,  4)) v = min(v, dseg(vec2(-0.500, -0.063), vec2(-0.500, -0.938)));
	if (bit(n,  5)) v = min(v, dseg(vec2(-0.438, -1.000), vec2(-0.063, -1.000)));
	if (bit(n,  6)) v = min(v, dseg(vec2( 0.063, -1.000), vec2( 0.438, -1.000)));
	if (bit(n,  7)) v = min(v, dseg(vec2( 0.500, -0.938), vec2( 0.500, -0.063)));
	if (bit(n,  8)) v = min(v, dseg(vec2( 0.063,  0.000), vec2( 0.438, -0.000)));
	if (bit(n,  9)) v = min(v, dseg(vec2( 0.063,  0.063), vec2( 0.438,  0.938)));
	if (bit(n, 10)) v = min(v, dseg(vec2( 0.000,  0.063), vec2( 0.000,  0.937)));
	if (bit(n, 11)) v = min(v, dseg(vec2(-0.063,  0.063), vec2(-0.438,  0.938)));
	if (bit(n, 12)) v = min(v, dseg(vec2(-0.438,  0.000), vec2(-0.063, -0.000)));
	if (bit(n, 13)) v = min(v, dseg(vec2(-0.063, -0.063), vec2(-0.438, -0.938)));
	if (bit(n, 14)) v = min(v, dseg(vec2( 0.000, -0.938), vec2( 0.000, -0.063)));
	if (bit(n, 15)) v = min(v, dseg(vec2( 0.063, -0.063), vec2( 0.438, -0.938)));
	ch_pos.x += ch_space.x;
	d = min(d, v);
}
mat2 rotate(float a)
{
	float c = cos(a);
	float s = sin(a);
	return mat2(c, s, -s, c);
}
vec3 hsv2rgb_smooth( in vec3 c )
{
    vec3 rgb = clamp( abs(mod(c.x*6.0+vec3(0.0,4.0,2.0),6.0)-3.0)-1.0, 0.0, 1.0 );

	rgb = rgb*rgb*(3.0-2.0*rgb); // cubic smoothing

	return c.z * mix( vec3(1.0), rgb, c.y);
}
void main( void )
{

	vec2 aspect = resolution.xy / resolution.y;
	uv = ( gl_FragCoord.xy / resolution.y ) - aspect / 2.0;
	float _d =  1.0-length(uv);
	uv *= 18.0 ;
	uv -= vec2(-7., 1.);
	//uv *= rotate(time+uv.x*0.05);

	vec3 ch_color = hsv2rgb_smooth(vec3(time*0.4+uv.y*0.1,0.5,1.0));

	vec3 bg_color = vec3(_d*0.4, _d*0.2, _d*0.1);
	uv.x += 0.5+sin(time+uv.y*0.7)*0.5;
	ch_pos = ch_start;


_ _ _ _ _ W O W _ nl1;
_ _ _ _  S O M E nl2;
_ _ _ _ T R O L L A G E nl3;



	vec3 color = mix(ch_color, bg_color, 1.0- (0.08 / d*2.0));  // shading
	fragColor = vec4(color, 1.0);
}
"""

fragment_shader = """
#version 400
//--- hatsuyuki ---
// by Catzpaw 2016
#ifdef GL_ES
precision mediump float;
#endif

//#extension GL_OES_standard_derivatives : enable
out vec4 fragColor;

uniform float time;
uniform vec2 mouse;
uniform vec2 resolution;

float snow(vec2 uv,float scale)
{
    float time1 = time / 10;
	float w=smoothstep(1.,0.,-uv.y*(scale/10.));
    if(w<.1){
        return 0.;
    }
	uv+=time1/scale;
    uv.y+=time1*2./scale;
    uv.x+=sin(uv.y+time1*.5)/scale;
	//uv*=scale;
    vec2 s=floor(uv),f=fract(uv),p;
    float k=3.,d;
	p=.5+.35*sin(11.*fract(sin((s+p+scale)*mat2(7,3,6,5))*5.))-f;
    d=length(p);
    k=min(d,k);
	k=smoothstep(0.,k,sin(f.x+f.y)*0.01);
    
    return k*w;
}

void main(void){
	vec2 uv=(gl_FragCoord.xy*2.-resolution.xy)/min(resolution.x,resolution.y); 
	vec3 finalColor=vec3(0);
	float c=smoothstep(1.,0.3,clamp(uv.y*.3+.8,0.,.75));
	//c+=snow(uv,30.)*.3;
	//c+=snow(uv,20.)*.5;
	//c+=snow(uv,15.)*.8;
	//c+=snow(uv,10.);
	//c+=snow(uv,8.);
	//c+=snow(uv,6.);
	c+=snow(uv,5.);
	finalColor=(vec3(c));
	fragColor = vec4(finalColor,1);
}

"""

fragment_shader = """
#version 400
//#extension GL_OES_standard_derivatives : enable

precision highp float;

uniform float time;
uniform vec2 mouse;
uniform vec2 resolution;

float random(float seed)
{
	return fract(sin(seed));//*200e2);
}


float row(float x, float y, float row_idx)
{
    float time1 = time*2;
	float rand_factor = 0.35+random(row_idx)*.175;
	return  step(0.3, y) * step(y, 0.37) * step(0.99, random(floor(x*rand_factor*-31.0 + 10.100*time1*random(rand_factor))));
}

void main()
{
	vec2 uv = gl_FragCoord.xy / resolution.y;
	uv.x *= 20.5;
	uv.y *= 20.0;
	
	float c = row(uv.y, fract(uv.x), floor(uv.x));
	
	gl_FragColor = vec4(c);
}
"""


fragment_shader = """
#version 400


out vec4 fragColor;

//uniform vec3      iResolution;           // viewport resolution (in pixels)
//uniform float     iTime;                 // shader playback time (in seconds)
//uniform float     iTimeDelta;            // render time (in seconds)
//uniform float     iFrameRate;            // shader frame rate
//uniform int       iFrame;                // shader playback frame
//uniform float     iChannelTime[4];       // channel playback time (in seconds)
//uniform vec3      iChannelResolution[4]; // channel resolution (in pixels)
//uniform vec4      iMouse;                // mouse pixel coords. xy: current (if MLB down), zw: click
//uniform samplerXX iChannel0..3;          // input channel. XX = 2D/Cube
//uniform vec4      iDate;                 // (year, month, day, time in seconds)
//uniform float     iSampleRate;           // sound sample rate (i.e., 44100)

 vec3      iResolution;           // viewport resolution (in pixels)
 float     iTime = 0;                 // shader playback time (in seconds)
 float     iTimeDelta = 1;            // render time (in seconds)
 float     iFrameRate = 1;            // shader frame rate
 int       iFrame;                // shader playback frame
 float     iChannelTime[4];       // channel playback time (in seconds)
 vec3      iChannelResolution[4]; // channel resolution (in pixels)
 vec4      iMouse;                // mouse pixel coords. xy: current (if MLB down), zw: click
 samplerXX iChannel0..3;          // input channel. XX = 2D/Cube
 vec4      iDate;                 // (year, month, day, time in seconds)
 float     iSampleRate = 1.;           // sound sample rate (i.e., 44100)
                


//Based on https://thebookofshaders.com/edit.php#11/wood.frag
float random (in vec2 st) {
    return fract(sin(dot(st.xy,
                         vec2(12.9898,78.233)))
                 * 43758.5453123);
}

// 2D Noise based on Morgan McGuire @morgan3d
// https://www.shadertoy.com/view/4dS3Wd
float noise (in vec2 st) {
    vec2 i = floor(st);
    vec2 f = fract(st);

    // Four corners in 2D of a tile
    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));
    // Smooth Interpolation
    // Cubic Hermine Curve.  Same as SmoothStep()
    vec2 u = f*f*(3.0-2.0*f);
    // u = smoothstep(0.,1.,f);
    // Mix 4 coorners percentages
    return mix(a, b, u.x) +
            (c - a)* u.y * (1.0 - u.x) +
            (d - b) * u.x * u.y;
}

mat2 rotate2d(float angle){
    return mat2(cos(angle),-sin(angle),
                sin(angle),cos(angle));
}

float lines(in vec2 pos, float b){
    float scale = 10.0;
    pos *= scale;
    return smoothstep(0.0,.5+b*.5,
                    abs((sin(pos.x*1.)+b*2.0))*0.95);
}

void main( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates <-0.5, 0.5>
    vec2 uv = (fragCoord - .5 * iResolution.xy) / iResolution.y;
    uv -= 1.;
    vec4 mouse = iMouse / iResolution.x;
    vec2 pos = vec2(uv*5.0) + mouse.xy*100.;
    float n = noise(pos)+iTime/100.;
    pos = rotate2d(n)*pos;
    float pattern = lines(pos,0.5);
    // Output to screen
    fragColor = vec4(vec3(pattern), 1.0) * vec4(0.55, 1.5,1.0,1.0);
}

"""
fragment_shader = """
#version 330

uniform vec2 resolution;
uniform float time;

//out vec4 outColor;
out vec4 fragColor;

precision highp float;

uniform sampler2D tex;

void main()
{
    vec2 uv = gl_FragCoord.xy/resolution;
	//float time = uTime * 0.4;

	// apply pixelate effect
	// vec2 uv_pixel = uv;
	vec2 uv_pixel = floor(uv * (resolution/4)) / (resolution/4);

    vec4 col1 = vec4(0.510, 0.776, 0.486, 1.0);
    vec4 col2 = vec4(0.200, 0.604, 0.318, 1.0);
    vec4 col3 = vec4(0.145, 0.490 ,0.278, 1.0);
    vec4 col4 = vec4(0.059, 0.255, 0.251, 1.0);

	// displacement on top of y
	vec3 displace = texture(tex, vec2(uv_pixel.x, (uv_pixel.y + time) * 0.05)).xyz;
	displace *= 0.5;
	displace.x -= 1.0;
	displace.y -= 1.0;
	displace.y *= 0.5;

	// color
	vec2 uv_tmp = uv_pixel;
	uv_tmp.y *= 0.2;
	uv_tmp.y += time;
    vec4 color = texture(tex, uv_tmp + displace.xy);

    // match to colors
    vec4 noise = floor(color * 10.0) / 5.0;
    vec4 dark   = mix(col1, col2, uv.y);
    vec4 bright = mix(col3, col4, uv.y);
    color = mix(dark, bright, noise);

	// add gradients (top dark and transparent, bottom bright)
    float inv_uv = 1.0 - uv_pixel.y;
    color.xyz -= 0.45 * pow(uv_pixel.y, 8.0);
    color.a -= 0.2 * pow(uv_pixel.y, 8.0);
    color += pow(inv_uv, 8.0);

    // make waterfall transparent
    color.a -= 0.2;

    fragColor = vec4(color);
}

"""
fragment_shader= """
#version 400

#define PI 3.1415926538
out vec4 fragColor;
uniform vec4 col2 = vec4(1);
uniform vec4 col3 = vec4(1,0,0,0);
uniform vec4 fix_bg = vec4(0,1,0,0);

uniform float fix1_size_x = 1 ;
uniform float fix1_speed_x = 0 ;
uniform float fix1_width_x = 1 ;
uniform float fix1_size_y = 1 ;
uniform float fix1_speed_y = 0 ;
uniform float fix1_width_y = 0.1 ;

uniform float fix3_size = 1 ;
uniform float fix3_speed = 0 ;
uniform float fix3_width = 0.1 ;

uniform float master_dim = 1;
uniform vec4 fix_block_pos = vec4(0,1,0,0);
uniform vec4 fix_circle_pos = vec4(0,1,0,0);
uniform vec2 resolution;
uniform float time;

float x_grid = 1;

vec4 ring(vec4 col,vec2 uv,vec2 aa, int z,float ang, float speed,float scaleX, float scaleY){
    //z =1; //count of star's
    //ang = 270;
    float t = time;
    for( float i=0.0; i < z; i++){

        float a = 0;
        a = ang/z * i * (PI/180)  ;
	    //a += time*speed;
        a += time/100*speed;

        float dy = cos(a) ;
        float dx = sin(a) ;

	    dy = dy * scaleY; // *.4; // scale y
	    dx = dx * scaleX; //*.9; // scale x
        dy += aa.y;
        dx += aa.x;
        if( i== 0){
            //col = vec2(dx,dy);
        }else{
            col += .30  / length(uv+vec2(dx,dy) );
        }
    }
        col *=  sin(vec4(0.4,0.8,0.9,1)  * time) * .35  +0.25;
    fragColor = col ;//vec4(col, 1.0);
    return col;
    //return fragColor;
}


vec4 circle(vec2 uv,vec4 col,vec2 a, float r, vec4 col2){
    //float t = 1.0 - smoothstep(0.0, 10, abs(r-1));
    if( distance( uv-a, vec2(0.5,0.5)) < r/2.0){
            col = col2;
    }
    return col;
}

vec4 circleS(vec2 uv,vec4 col,vec2 a, float r, vec4 col2){
    float borderThickness = 2;
    float d = 1;
    vec3 color = vec3(1,1,0);
    vec3 baseColor = vec3(1,1,0);
    float t1 = 1.0 - smoothstep(r-borderThickness, r, d);
    float t2 = 1.0 - smoothstep(r, r+borderThickness, d);
    return vec4(mix(color.rgb, baseColor.rgb, t1), t2);
}

vec4 block(vec2 uv,vec4 col, vec2 a, vec2 b, vec4 col2){
    float r1 = 0;
    float boarder = 5;
    float x1 = uv.x-a.x;
    float x2 = uv.x-a.x+b.x;
    if( uv.x > a.x-b.x/2 && uv.x < a.x+b.x/2 ){
       
        float y1 = uv.y-a.y;
        float y2 = uv.y-a.y+b.y;

        float r2 = 0;
        if( uv.y > a.y-b.y/2 && uv.y < a.y+b.y/2 ){
            col = col2;
            //col.r = 1    ; //time ;//vec4(0,time, 0,1);
            //col.g = 0.0  ;//time ;//vec4(0,time, 0,1);
            //col.b = 1.1  ;//time ;//vec4(0,time, 0,1);
            //col.a = 1.0;
            //col *= 0.2+(r1*r2) ;//(r1 * r2);
            //col[3] += time*10 ;//vec4(0,time, 0,1);
            if( r2< 1){
                r2 += 0.2;
            }
        }
        if( r1 < 1){
            r1 += 0.2;
        }
    }
    if( uv.y == a.y ){ //|| uv.x == a.x ){
        col.r = 1    ; //time ;//vec4(0,time, 0,1);
        col.g = 1  ;//time ;//vec4(0,time, 0,1);
        col.b = 0  ;//time ;//vec4(0,time, 0,1);
        col.a = 1.0;
    }
    return col;
}

vec4 block1(vec2 uv,vec4 col, vec2 a, vec2 b){
    if( uv.x > a.x && uv.x < a.x+b.x ){
        if( uv.y > a.y && uv.y < a.y+b.y ){
            col.r = 0 ;//time ;//vec4(0,time, 0,1);
            col.g = 0.5 ;//time ;//vec4(0,time, 0,1);
            col.b = 0.9 ;//time ;//vec4(0,time, 0,1);
            col.a = 1.0;
            //col[3] += time*10 ;//vec4(0,time, 0,1);
        }
    }
    return col;
}

vec4 pulse(vec2 uv,vec4 col, vec2 a,vec4 col4){
    float tt = sin(time*10)*1000;
    col = circle(uv,col,a,tt,col4);
    col4 = vec4(0,0,0,1);
    col = circle(uv,col,a,tt-100,col4);

    tt = cos(time)*1000;
    col4 = vec4(1,0,0,1);
    col = circle(uv,col,a,tt-300,col4);
    col4 = vec4(0,0,0,1);
    col = circle(uv,col,a,tt-310,col4);
    return col;
}

float grid(vec2 st, float res){
  vec2 grid = fract(st*res);
  return (step(res,grid.x) * step(res,grid.y));
}

float random(float seed){
	return fract(sin(seed)*1e4);
}


uniform float direction;
uniform float velocity = 1.0;
uniform float intensity;
    
    //vec3 COLOR = vec3(1);
    //vec3 finalColor = vec3(1);

float snow(vec2 uv, float scale, float time)
{
    float w=smoothstep(1.0,0.0,-uv.y*(scale/10.0));if(w<.1)return 0.0;
    uv+=time/scale;uv.y+=time*2.0/scale;uv.x+=sin(uv.y+time*.5)/scale;
    uv*=scale;vec2 s=floor(uv),f=fract(uv),p;float k=3.0,d;
    p=.5+.35*sin(11.0*fract(sin((s+scale)*mat2(vec2(7,3),vec2(6,5)))*5.0))-f;d=length(p);k=min(d,k);
    k=smoothstep(0.0,k,sin(f.x+f.y)*0.01);
    return k*w;
}

void main1(){;
    vec2 uv = gl_FragCoord.xy ; //vUV.st ;
    //vec2 uv = (gl_FragCoord.xy - resolution.xy/2) / resolution.y;
    uv -= resolution.xy/2;
    float r = 0.17;

    vec2 a = vec2(200,0);
    vec2 b = vec2(50,50);

    
    int z = 10;
    float ang = 360;
    float speed = .9;
    uv.x = uv.x * 2 -1;
    uv.y = uv.y * 2 -1;
    uv += vec2(0,1);
    uv.x += 1;
    vec4 col = vec4(0,0,0,1);
    vec4 col4 = vec4(0,1,0,1);
    

    col = fix_bg ; //col44; 
    
    //float c=smoothstep(1.0,0.3,clamp(uv.y*0.3+0.8,0.0,0.75));
    //c  += snow(uv,30,time);
    //col += vec4(vec3(c),0.5);
    
    if(0==1){
    float TIME = fix1_speed_x/20;
    //float c=smoothstep(1.0,0.3,clamp(uv.y*.3+.8,0.0,.75));
    float c=smoothstep(1.0,0.3,clamp(uv.y+.8,0.0,.75));
    c+=snow(uv,30.0,TIME)*.3;
    //c+=snow(uv,20.0,TIME)*.5;
    //c+=snow(uv,15.0,TIME)*.8;
    //c+=snow(uv,10.0,TIME);
    //c+=snow(uv,8.0,TIME);
    c+=snow(uv,6.0,TIME);
    //c+=snow(uv,5.0,TIME);
    vec3 finalColor=vec3(c);
    col = vec4(finalColor,1.0);
    }
    //# background animation
    float _fix1_width_x = fix1_width_x/10;
    if( fix1_width_x <= 1){
       _fix1_width_x = 1;
    }
    float _fix1_width_y = fix1_width_y/10;
    if( fix1_width_y <= 1){
       _fix1_width_y = 1;
    }

    float mysin1 = sin((uv.y+fix1_speed_y)/_fix1_width_y)*fix1_size_y;
    float mysin2 = sin((uv.x+fix1_speed_x)/_fix1_width_x)*fix1_size_x;

    float dir = -1;
    if( uv.x > (resolution.x/2) ){ //resolution.x/2 ){
        //col = vec4(0,0,0,0);
        //mysin1 = 0;
        float mysin1 = sin((uv.y+fix1_speed_y)/_fix1_width_y)-fix1_size_y;
    }
    mysin2 *= dir;

    //float mysin2 = clamp(uv.x/3.14/10+fix2_speed*4+sin(fix2_width/10))*fix2_size;
    //float mysin2 = smoothstep(uv.x/3.14/10+fix2_speed*4+sin(fix2_width/10))*fix2_size;
    //float mysin2 = fract(uv.x/3.14/10+fix2_speed*4+sin(fix2_width/10))*fix2_size;
    //float mysin2 = length(uv/3.14/10+fix2_speed*4+sin(fix2_width/10))*fix2_size;

    mysin1 += cos((uv.y+.1+fix3_speed)/fix3_width/2)*fix3_size ;//mysin1*-1; //a*4;
    //mysin2 *= 6;
    col -= vec4(mysin1*fix_bg.r ,mysin1*fix_bg.g ,mysin1*fix_bg.b , 1 ) ;
    col -= vec4(mysin2*fix_bg.r ,mysin2*fix_bg.g ,mysin2*fix_bg.b , 1 ) ;
    

    col = circle(uv,col,vec2(20,20),40,vec4(0,1,1,0));
    col = circle(uv,col,vec2(0,0),20,vec4(0,1,0,0));
    //vec4 circle(vec2 uv,vec4 col,vec2 a, float r, vec4 col2){

    vec2 grid_uv = vec2(uv.xy*0.5);
    float x = grid( grid_uv, 1/15.) ;
    //col.rgb -= vec3(x,x,x) ;//*x;

    a = vec2(0,0);

    col4 = vec4(1,0,0,1);
    a = vec2(600,0);

    col += 0.1 / length(uv+vec2(.6,.8) ); //sun



    //# BOX
    a.x += sin(time*2)*100*3;
    a.y += cos(time*2)*100*3;
    b = vec2(100,200);
    vec2 aa = vec2(0,0);
    aa.x = fix_block_pos.x -255*2;
    aa.y = fix_block_pos.y -255*2;
    col = block(uv,col,aa,b,col2);

    a = vec2(0,0);
    b = vec2(100,200);
    
    a.x += cos(time*2)*100*3;
    a.y += sin(-1*time*2)*100*3;
    aa.x = fix_circle_pos.x -255*2;
    aa.y = fix_circle_pos.y -255*2;
    col = circle(uv,col,aa,100,col3);

    a.x += cos(time*2+.1)*100*3;
    a.y += sin(-1*time*2+.1)*100*3;
    col4 = vec4(1,0,1,0);
    col4 = vec4(1,0,1,0);

    a.x = cos(time*2-.3)*100*4;
    a.y = sin(-1*time*2-.3)*100*2;
    a.y *=-1;
    col4 = vec4(1,1,0,0);
    
    //float dist = distance(uv , vec2(10,10));
    //float circle = smoothstep((10-0.01),(10+0.01),1.0-dist );

    //# Planet's
    a.x = -1000;
    z = 20; //count of star's
    ang = 360;
    speed = 50;
    a = vec2(500,100);
    //col = ring(col,uv,a, z, ang, speed, 180, 180)*4;

    ang = 360;
    speed = 50;
    //col = ring(col,uv,a, z, ang, -speed, 280, 280/2)*2;

    
    //col *= length(master_dim);
    //col *= 0.5;
    col *= master_dim;

    //# blue background
    fragColor = col ;//vec4(col,1);
}

void main2(){
    vec2 uv = gl_FragCoord.xy ; //vUV.st ;
    uv -= resolution.xy/2;
    vec4 col = vec4(0,0,0,1);

    if( uv.x > -100 && uv.x < 100 ){
        col.b = 1 ;//length(vec2(2.9,0.9) )/200;
    }
    fragColor = col ;//vec4(col,1);
}

void main(){
    main1();
    //main2();
}
"""


import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

mc.set("some_key", "Some value")
value = mc.get("some_key")

mc.set("another_key", 3)
mc.delete("another_key")

import time
import json
data = {}
start = time.time()
delta = start

def mc_loop():
    ch = 141
    send = 0
    #cmd="stats items" 
    x=mc.get("index")#cmd)
    if x:
        #print(x)
        print()
        for k,v in x.items():
            #print(k,v)
            x=mc.get(k)
            print(k,v,ch,"=",x[ch-1])
    time.sleep(.13)



import math

class Screen(mglw.WindowConfig):
    window_size = 600, 300
    window_size = 900, 506
    window_size = 1024, 768
    #window_size = 1900, 1070
    #resource_dir = 'programms'

    def __init__(self,**args):
        super().__init__(**args)

        self.quad = mglw.geometry.quad_fs()
        print(dir(self.quad))
        # load shader's as string
        self.prog = self.ctx.program(vertex_shader=vertex_shader,
                                      fragment_shader=fragment_shader)
        # load shader's form file
        print(dir(self.prog))
        #self.prog = self.load_program(vertex_shader='vertex_shader.gls1',
        #                              #fragment_shader='fragment_shader.gls1')

        self.set_uniform('resolution',self.window_size)
        self.t = time.time()
        self.ANG = 0
        self.ANG_DIR = 1
        self.time = 0

        self.fix1_speed_x = 0
        self.fix1_speed_y = 0
        self.fix3_speed = 0

    def set_uniform(self,u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except KeyError:
            print(f'uniform: {u_name} - not used in shader')

    def render(self,_time,frame_time):
        self.set_uniform('resolution',self.window_size)
        self.ctx.clear()
        _t = _time % 600 # max cycle time 10minutes 
        
        #self.set_uniform('time',_t)
        if self.ANG_DIR:
            self.ANG += 0.01
        else:
            self.ANG -= 0.01

        if self.ANG <= -2:
            self.ANG_DIR = 1
            self.ANG = -2
        elif self.ANG >= 3.1415:
            #self.ANG_DIR = 0
            self.ANG = 0
        a = self.ANG
        #a = math.sin(a ) #math.radians(a) )
        x = mc.get("2.0.0.13:2")
        if not x:
            x = mc.get("10.10.10.13:2")
        
        if not x:
            x=[1]*512

        r = 1 #255
        g = 0
        b = 1 #255
        aa=0
        bb=0
        if x:
            #a = 1+x[141-1]/255.*10
            r = x[142-1]/255
            g = x[143-1]/255
            b = x[144-1]/255
            aa = x[145-1] *4 #* a
            bb = x[146-1] *4 #* a
            self.time += (x[148-1]/255.-0.5)/10 # *4 #* a

        self.set_uniform('time',self.time)

        self.set_uniform('fix_block_pos',[aa,bb,0,0])
        self.set_uniform('fix_circle_pos',[bb,aa,0,0])

        dmx=141-1
        print(x[dmx],x[dmx+1],x[dmx+2])
        self.set_uniform('master_dim',x[dmx]/255.)

        dmx=161-1
        print(x[dmx],x[dmx+1],x[dmx+2])

        dmx=201-1
        print(dmx+1,x[dmx:dmx+8])
        self.set_uniform('fix1_size_x',x[dmx]/255.*6)
        self.set_uniform('fix1_size_y',x[dmx+1]/255.*6)
        self.fix1_speed_x += (x[dmx+2]/255.-0.5)*300
        self.fix1_speed_y += (x[dmx+3]/255.-0.5)*300
        self.set_uniform('fix1_speed_x',self.fix1_speed_x) 
        self.set_uniform('fix1_speed_y',self.fix1_speed_y) 
        self.set_uniform('fix1_width_x',x[dmx+4]*2)
        self.set_uniform('fix1_width_y',x[dmx+5]*2)

        dmx=121-1
        print(dmx+1,x[dmx:dmx+8])
        self.set_uniform('fix3_size',x[dmx]/255.*6)
        self.fix3_speed += (x[dmx+1]/255.-0.5)*300
        self.set_uniform('fix3_speed',self.fix3_speed)
        self.set_uniform('fix3_width',x[dmx+2]*2)


        x = time.time()/10%1
        #self.set_uniform('col2',[r,g,b,1])
        self.set_uniform('fix_bg',[r,g,b,1])
        self.set_uniform('col2',[1,x,0,1])
        self.quad.render(self.prog)

        if self.t+1 < time.time():
            print("_time",round(_time,2),"_t",round(_t,2),"self.ANG",round(self.ANG,2))
            self.t = time.time()

if __name__ == "__main__":
    mglw.run_window_config(Screen)

