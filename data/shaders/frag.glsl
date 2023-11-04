#version 330 core

uniform sampler2D tex;
uniform sampler2D noise;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void main() {
    //vec2 texCoords = vec2(uvs.x + sin(time * 0.01 + uvs.y) * 0.01, uvs.y + sin(time * 0.01 + uvs.x) * 0.01);
    vec3 mult = texture(noise, uvs - (time * 0.0001)).rgb;
    mult.rgb += sin(mult.rgb * 60 + 100 * sin(time * 0.0000001)) * 0.1;
    if (mult.r < 0.2) {
        vec3 color = vec3(0.4, 0.4, 0.0);
        mult.rgb = color;
    }
    else if (mult.r < 0.4) {
        vec3 color = vec3(0.4, 0.0, 0.0);
        mult.rgb = color;
    }
    else if (mult.r < 0.8) {
        vec3 color = vec3(0.0, 0.0, 0.0);
        mult.rgb = color;
    }
    f_color = vec4(texture(tex, uvs).rgb + mult, 1.0);
}