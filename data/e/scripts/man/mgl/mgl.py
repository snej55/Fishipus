import moderngl, array, pygame

default_vert = """
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert.x, vert.y, 0.0, 1.0);
}
"""

default_frag = """
#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main() {
    f_color = vec4(texture(tex, uvs).rgb, 1.0);
}
"""

class MGL:
    def __init__(self, app, frag_path=None, vert_path=None):
        self.ctx = moderngl.create_context()
        self.quad_buffer = self.ctx.buffer(data=array.array('f', [
                                        -1.0, 1.0, 0.0, 0.0,
                                        1.0, 1.0, 1.0, 0.0,
                                        -1.0, -1.0, 0.0, 1.0,
                                        1.0, -1.0, 1.0, 1.0
                                    ]))
        frag = default_frag
        vert = default_vert
        if frag_path:
            frag = open('data/shaders/' + frag_path, 'r').read()
        if vert_path:
            vert = open('data/shaders/' + vert_path, 'r').read()
        self.program_vert = vert
        self.program_frag = self.ctx.program(vertex_shader=vert, fragment_shader=frag)
        self.temp_texs = []
        self.render_objects = self.ctx.vertex_array(self.program_frag, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def surf_to_texture(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex
    
    def parse_uniforms(self, uniforms):
        for name, value in uniforms.items():
            if type(value) == pygame.Surface:
                tex = self.surf_to_texture(value)
                uniforms[name] = tex
                self.temp_texs.append(tex)
        return uniforms
    
    def update(self, screen, uniforms):
        tex_id = 0
        unis = list(self.program_frag)
        for uniform in uniforms:
            if uniform in unis:
                if type(uniforms[uniform]) == moderngl.Texture:
                    uniforms[uniform].use(tex_id)
                    self.program_frag[uniform] = tex_id
                    tex_id += 1
                else:
                    self.program_frag[uniform] = uniforms[uniform]
    
    def draw(self, surf, uniforms={}):
        uniforms = self.parse_uniforms(uniforms)
        uniforms['tex'] = self.surf_to_texture(surf)
        self.temp_texs.append(uniforms['tex'])
        self.update(surf, uniforms)
        self.render_objects.render(mode=moderngl.TRIANGLE_STRIP)
        for tex in self.temp_texs:
            tex.release()
        self.temp_texs = []
