#version 330 core

uniform sampler2D tex;
uniform sampler2D noise;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void main() {
    //vec2 texCoords = vec2(uvs.x)
    vec3 mult = sin(texture(noise, uvs + (time * 0.0001)).rgb + time * 0.01);
    f_color = vec4(texture(tex, uvs).rgb + mult, 1.0);
}