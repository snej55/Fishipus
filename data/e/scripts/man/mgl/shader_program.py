class ShaderProgram:
    def __init__(self, ctx, mgl, shader_name):
        self.ctx = ctx
        self.mgl = mgl
        self.vbo = mgl.vbo
        self.program = self.get_program(shader_name)
    
    def get_vao(self):
        vao = self.ctx.vertex_array(self.program, [(self.vbo, '2f 2f', 'vert', 'texcoord')])
        return vao
    
    def get_program(self, shader_name):
        with open(f'data/shaders/{shader_name}.vert') as f:
            vertex_shader = f.read()
        with open(f'data/shaders/{shader_name}.frag') as f:
            fragment_shader = f.read()
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program