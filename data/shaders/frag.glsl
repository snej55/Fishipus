#version 330 core

uniform sampler2D tex;
// use a different noise texture e.g: different scale, detail, size, octaves, levels
uniform sampler2D noise;
uniform float time;
// scroll (obsolete)
uniform vec2 camera;

in vec2 uvs; // pixel coordinates
out vec4 f_color;  // pixel color

uniform float timeScale = 0.00025;  // time speed
// messy stuff ---------
uniform float angleConst = 1.5;
uniform float stripeImpact = 0.03;
uniform float stripeWidth = 60;
// ---------------------
uniform float threshold = 0.34; // size of hole

void main() {
    float centerDis = distance(vec2(0.5, 0.5), uvs);
    centerDis = centerDis * centerDis * centerDis * centerDis * 0.2;
    vec2 texCoords = vec2(uvs.x, uvs.y);  // can be used to warp screen 
    // manipulate noise texture based on time --------------------------------------------------
    vec2 shiftTexcoords = vec2(texCoords.x + sin(time * 0.2 * timeScale), texCoords.y * 2.0 - sin(time * 0.02 * timeScale)); // change stuff here
    vec4 color1 = texture(noise, shiftTexcoords);
    
    shiftTexcoords = vec2(texCoords.x * 2.7 - sin(time * 0.05 * timeScale), texCoords.y * 1.7 - sin(time * 0.5 * timeScale)); // and here
    vec4 color2 = texture(noise, shiftTexcoords);

    shiftTexcoords = vec2(texCoords.x * 0.35 - sin(time * 0.4 * timeScale), texCoords.y * 0.35 - sin(time * 0.4 * timeScale)); // here as well
    vec4 color3 = texture(noise, shiftTexcoords);
    // -----------------------------------------------------------------------------------------

    // some funky math
    vec4 combinedColor = (color1 + color2 * 0.5 + color3 * 0.5) * 0.5;
    combinedColor = combinedColor * (distance(vec2(0.5, 0.5), texCoords) * 0.5 + 0.5) + sin((texCoords.x - texCoords.y * angleConst) * stripeWidth) * stripeImpact;

    vec4 baseColor;
    if (combinedColor.r < threshold - 0.03) {
        // reflections
        float center_dis =  (distance(vec2(0.5, 0.5), texCoords * 5) - 0.5) * 0.2 + 0.8;
        vec2 reflectionCoords = vec2((texCoords.x - 0.5) * center_dis + 0.5, (texCoords.y - 0.5) * center_dis + 0.5);
        vec4 reflectionColor = texture(tex, reflectionCoords) * (0.5 - centerDis);
        if (reflectionColor.a == 0) {
            baseColor = vec4(0.025 + reflectionColor.g * 0.1, 0.025 + reflectionColor.b * 0.1, 0.045 + reflectionColor.r * 0.1, 1.0);//baseColor = vec4(0.012, 0.012, 0.025, 1.0);
        } else {
            baseColor = vec4(0.025 + reflectionColor.g * 0.1, 0.025 + reflectionColor.b * 0.1, 0.045 + reflectionColor.r * 0.1, 1.0);
        }
    } else if (combinedColor.r < threshold + 0.01) {
        baseColor = vec4(0.0, 0.0, 0.01, 1.0);  // different colors
    } else if (combinedColor.r < threshold + 0.02) {
        baseColor = vec4(0.2, 0.2, 0.34, 1.0);
    } else if (combinedColor.r < threshold + 0.05) {
        baseColor = vec4(0.11, 0.118, 0.176, 1.0);
    } else if (combinedColor.r < threshold + 0.1) {
        baseColor = vec4(0.05, 0.05, 0.09, 1.0);
    } else {
        baseColor = vec4(0.025, 0.025, 0.045, 1.0);
    }

    // check if part of background
    float alpha = (texture(tex, texCoords).r + texture(tex, texCoords).g + texture(tex, texCoords).b) * 0.333;
    if (alpha > 0.01) {
        baseColor = texture(tex, texCoords);
    }
    // vignait effect
    baseColor = baseColor - centerDis;
    f_color = vec4(baseColor.rgb, 1.0);
}