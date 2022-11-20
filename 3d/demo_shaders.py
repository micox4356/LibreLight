

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
#version 430

in vec3 in_position;

void main(){
    gl_Position = vec4(in_position, 0.9);
}
"""



fragment_shader = """
#version 450

#define PI 3.1415926538
out vec4 fragColor;

uniform vec2 resolution;
uniform float time;

vec4 ring(vec4 col,vec2 uv, int z,float ang, float speed,float scaleX, float scaleY){
    //z =1; //count of star's
    //ang = 270;
    float t = time;
    for( float i=0.0; i < z; i++){

        float a = 0;
        a = ang/z * i * (PI/180)  ;
	    //a += time*speed;
        a += time/100*speed;

        float dy = cos(a);
        float dx = sin(a);

	    dy = dy * scaleY; // *.4; // scale y
	    dx = dx * scaleX; //*.9; // scale x
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
vec4 block(vec2 uv,vec4 col, vec2 a, vec2 b){
    if( uv.x > a.x && uv.x < a.x+b.x ){
        if( uv.y > a.y && uv.y < a.y+b.y ){
            col.r = 0 ;//time ;//vec4(0,time, 0,1);
            col.g = 0.5 ;//time ;//vec4(0,time, 0,1);
            col.b = 0.9 ;//time ;//vec4(0,time, 0,1);
            //col[3] += time*10 ;//vec4(0,time, 0,1);
        }
    }
    return col;
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

    col += 0.1 / length(uv+vec2(.6,.8) ); sun

    # background animation
    float mysin = sin(uv.x/3.14/20*time);
    float mysin2 = sin(uv.y/3.14/20*time*4);
    float mycos = cos(uv.x/3.14/10*time);
    col += vec4(mysin2,0, 0,1);
    //col += vec4(mysin-mysin2,0, 0,1);


    # BOX
    a.x += sin(time*2)*100*3;
    a.y += cos(time*2)*100*3;
    //b.y += 150+time*100;
    col = block(uv,col,a,b);

    a = vec2(0,0);
    b = vec2(100,200);
    
    a.x += cos(time*2)*100*3;
    a.y += sin(-1*time*2)*100*3;
    //b.y += 150+time*100;
    col = block(uv,col,a,b);
    //col.r -= 0.1; 

    
    float dist = distance(uv , vec2(10,10));
    float circle = smoothstep((10-0.01),(10+0.01),1.0-dist );

    # Planet's
    z = 20; //count of star's
    ang = 360;
    speed = 50;
    col = ring(col,uv, z, ang, speed, 180, 180)*4;

    z = 80; //count of star's
    ang = 360;
    speed = 50;
    col = ring(col,uv, z, ang, -speed, 280, 280/2)*2;

    
    # blue background
    if( uv.x > -100 && uv.x < 100 ){
        col.b = 1 ;//length(uv+vec2(2.9,0.9) )/200;
    }
    
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

import math

class Screen(mglw.WindowConfig):
    window_size = 600, 300
    window_size = 900, 506
    #window_size = 1200, 900
    #window_size = 1900, 1070
    #resource_dir = 'programms'

    def __init__(self,**args):
        super().__init__(**args)

        self.quad = mglw.geometry.quad_fs()
        # load shader's as string
        self.prog = self.ctx.program(vertex_shader=vertex_shader,
                                      fragment_shader=fragment_shader)
        # load shader's form file
        #self.prog = self.load_program(vertex_shader='vertex_shader.gls1',
        #                              #fragment_shader='fragment_shader.gls1')

        self.set_uniform('resolution',self.window_size)
        self.t = time.time()
        self.ANG = 0
        self.ANG_DIR = 1

    def set_uniform(self,u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except KeyError:
            print(f'uniform: {u_name} - not used in shader')

    def render(self,_time,frame_time):
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

        self.set_uniform('time',a)
        self.quad.render(self.prog)

        if self.t+1 < time.time():
            print(_time,_t,self.ANG)
            self.t = time.time()

if __name__ == "__main__":
    mglw.run_window_config(Screen)

