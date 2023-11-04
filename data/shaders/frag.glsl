#version 330 core

uniform sampler2D tex;
uniform sampler2D noise;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec3 mult = texture(noise, uvs + (time * 0.0001)).rgb;
    f_color = vec4(texture(tex, uvs).rgb * mult, 1.0);
}