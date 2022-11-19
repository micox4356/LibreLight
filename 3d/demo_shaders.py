

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
#version 430

out vec4 fragColor;

uniform vec2 resolution;
uniform float time;

vec2 rotate2D(vec2 uv, float a){
    float s = sin(a);
    float c = cos(a);
    return mat2(c,-s,s,c) * uv;
}
vec3 ring(vec3 col,vec2 uv, int z,float ang, float speed,float scaleX, float scaleY){
    //z =1; //count of star's
    //ang = 270;
    for( float i=0.0; i < z; i++){

        float a = 0;
        a = ang/z * i * (3.1415/180)  ;
	    a += time*speed;

        float dy = cos(a)/2;
        float dx = sin(a)/2;

	    dy = dy * scaleY; // *.4; // scale y
	    dx = dx * scaleX; //*.9; // scale x
        col += 0.01  / length(uv+vec2(dx+0.1,dy) );
    }
    col *=  sin(vec3(0.2,0.8,0.9)  * time) * 0.15  +0.25;
    fragColor = vec4(col, 1.0);
    return col;
    //return fragColor;
}

void main() {
    vec2 uv = (gl_FragCoord.xy - resolution.xy/2) / resolution.y;
    vec3 col = vec3(0.0);
    
    //uv = rotate2D(uv, 3.14/2.0+3.2);
    //uv = rotate2D(uv, 3.14/2.0);

    float r = 0.17;
    
    int z = 10;
    float ang = 360;
    float speed = .9;

    z = 50; //count of star's
    ang = 270;
    speed = -.1;
    col = ring(col,uv, z, ang, speed, .9, .4);
    
    z = 10;
    //col = ring(col,uv, z, 270,0.1, .7, .7);


    z =2; //count of star's
    ang = 90;
    speed = 10;
    col = ring(col,uv, z, ang, speed, .6, .2);



    z = 20; //count of star's
    ang = 360;
    speed = 0.5;
    col = ring(col,uv, z, ang, speed, .5, .5);


/*
    float i = 0;
    float a = time+i;
    a = ang/z * i * (3.1415/180)  ;
    a += time/4;
    float dx = 0.1;//cos(a)/2;
    float dy = 0.1;//sin(a)/2;
    //col += 0.01 / length(uv+vec2(dx+0.1,dy) );
    col += 0.03 / length(uv+vec2(dx+0.5,dy) );
    //col *= sin(vec3(0.8,0.2,0.9) * time) * 0.15 +0.25;
    fragColor = vec4(col, 1.0);
    dx = 0.2;
    dy = 0.42;
    col += 0.01 / length(uv+vec2(dx+0.5,dy) );
    fragColor = vec4(col, 1.0);

    uv + vec2(0,0);
    col = vec3(0.0);
    //fragColor = vec4(vec3(0,0,1), 1.0);
    //fragColor[0] = [0,0,1,1];
*/
}



"""

vertex_shader2 = """
#version 450

in vec3 in_position;

void main(){
    gl_Position = vec4(in_position, 0.9);

    const vec3 positions[3] = vec3[3](
		vec3(1.f,1.f, 0.0f),
		vec3(-1.f,1.f, 0.0f),
		vec3(0.f,-1.f, 0.0f)
	);

	//output the position of each vertex
	//gl_Position = vec4(positions, 1.0f);
	//gl_Position = vec4(1.f,1.f, 0.0f, 1.0f);
	//gl_Position = vec4(-1.f,1.f, 0.0f, 1.0f);
	//gl_Position = vec4(1.f,-1.f, 0.0f, 1.0f);
	//gl_Position = vec4(positions[gl_VertexIndex], 1.0f);
}
"""

fragment_shader2 = """
#version 450

out vec4 fragColor;

uniform vec2 resolution;
uniform float time;

void main(){
    vec2 uv = (gl_FragCoord.xy - resolution.xy/2) / resolution.y;
    vec3 col = vec3(0.0);
	fragColor = vec4(1.f,0.f,0.f,1.0f);

}
"""


class Screen(mglw.WindowConfig):
    window_size = 600, 300
    window_size = 900, 506
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

    def set_uniform(self,u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except KeyError:
            print(f'uniform: {u_name} - not used in shader')

    def render(self,_time,frame_time):
        self.ctx.clear()
        self.set_uniform('time',_time)
        if self.t+10 < time.time():
            print(_time)
            self.t = time.time()
        self.quad.render(self.prog)

if __name__ == "__main__":
    mglw.run_window_config(Screen)

