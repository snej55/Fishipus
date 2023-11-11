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
        self.app = app
        self.ctx = moderngl.create_context(require=330)
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y) , texture coordinates (x, y)
            -1.0, 1.0, 0.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, 1.0, 1.0, 0.0,
            1.0, -1.0, 1.0, 1.0,
        ]))
        self.quad_buffer_notex = self.ctx.buffer(data=array('f', [
            # position (x, y)
            -1.0, 1.0,
            -1.0, -1.0,
            1.0, 1.0,
            1.0, -1.0,
        ]))
        self.default_frag = default_frag
        self.default_vert = default_vert
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
    
    def default_ro(self):
        return RenderObject(self.app, self, self.default_frag, default_ro=True)
    
    @staticmethod
    def texture_update(tex, surf):
        tex.write(surf.get_view('1'))
        return tex

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

class RenderObject:
    def __init__(self, app, mgl, frag_shader, vert_shader=None, vao_args=['2f 2f', 'vert', 'texcoord'], buffer=None, default_ro=False):
        self.app = app
        self.mgl = mgl
        self.ctx = mgl.ctx
        self.default_ro = default_ro
        self.vert_shader = vert_shader
        if not vert_shader:
            self.vert_shader = default_vert
        self.frag_shader = frag_shader
        self.vao_args = vao_args
        self.program = self.ctx.program(vert_shader=self.vert_shader, frag_shader=self.frag_shader)
        if not buffer:
            buffer = self.mgl.quad_buffer
        self.vao = self.mgl.ctx.vertex_array(self.program, [(buffer, *vao_args)])
        self.temp_texs = []

    def parse_uniforms(self, uniforms):
        for name, value in uniforms.items():
            if type(value) == pygame.Surface:
                tex = self.surf_to_texture(value)
                uniforms[name] = tex
                self.temp_texs.append(tex)
        return uniforms
    
    def update(self, uniforms={}):
        tex_id = 0
        uniform_list = list(self.program)
        for uniform in uniforms:
            if uniform in uniform_list:
                if type(uniforms[uniform]) == moderngl.Texture:
                    uniforms[uniform].use(tex_id)
                    self.program[uniform].value = tex_id
                    tex_id += 1
                else:
                    self.program[uniform].value = uniforms[uniform]

    def render(self, dest=None, uniforms={}):
        if not dest:
            dest = self.mgl.ctx.screen
            
        dest.use()
        uniforms = self.parse_uniforms(uniforms)
        self.update(uniforms=uniforms)
        self.vao.render(mode=moderngl.TRIANGLE_STRIP)
        
        for tex in self.temp_textures:
            tex.release()
        self.temp_textures = []