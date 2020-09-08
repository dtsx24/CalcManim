from manimlib.imports import *
#Para versiones anteriores de manim usar:
#from big_ol_pile_of_manim_imports import *


#### SUGERENCIA: SIEMPRE QUE CAMBIESLOS VECTORES A VISUALIZAR ###
### CONSIDERA QUE EL PLNO ES DE [-7,7]x[-4,4] ####

#### ESTE GRID SOLO SE USA PARA LA CLASE BOLAS ####

class Grid(VGroup):
    CONFIG = {
        "height": 6.0,
        "width": 6.0,
    }

    def __init__(self, rows, columns, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        x_step = self.width / self.columns
        y_step = self.height / self.rows

        for x in np.arange(0, self.width + x_step, x_step):
            self.add(Line(
                [x - self.width / 2., -self.height / 2., 0],
                [x - self.width / 2., self.height / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width / 2., y - self.height / 2., 0],
                [self.width / 2., y - self.height / 2., 0]
            ))

class ScreenGrid(VGroup):
    CONFIG = {
        "rows": 8,
        "columns": 14,
        "height": FRAME_Y_RADIUS * 2,
        "width": 14,
        "grid_stroke": 0.5,
        "grid_color": WHITE,
        "axis_color": RED,
        "axis_stroke": 2,
        "labels_scale": 0.25,
        "labels_buff": 0,
        "number_decimals": 2
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rows = self.rows
        columns = self.columns
        grid = Grid(width=self.width, height=self.height, rows=rows, columns=columns)
        grid.set_stroke(self.grid_color, self.grid_stroke)

        vector_ii = ORIGIN + np.array((- self.width / 2, - self.height / 2, 0))
        vector_si = ORIGIN + np.array((- self.width / 2, self.height / 2, 0))
        vector_sd = ORIGIN + np.array((self.width / 2, self.height / 2, 0))

        axes_x = Line(LEFT * self.width / 2, RIGHT * self.width / 2)
        axes_y = Line(DOWN * self.height / 2, UP * self.height / 2)

        axes = VGroup(axes_x, axes_y).set_stroke(self.axis_color, self.axis_stroke)

        divisions_x = self.width / columns
        divisions_y = self.height / rows

        directions_buff_x = [UP, DOWN]
        directions_buff_y = [RIGHT, LEFT]
        dd_buff = [directions_buff_x, directions_buff_y]
        vectors_init_x = [vector_ii, vector_si]
        vectors_init_y = [vector_si, vector_sd]
        vectors_init = [vectors_init_x, vectors_init_y]
        divisions = [divisions_x, divisions_y]
        orientations = [RIGHT, DOWN]
        labels = VGroup()
        set_changes = zip([columns, rows], divisions, orientations, [0, 1], vectors_init, dd_buff)
        for c_and_r, division, orientation, coord, vi_c, d_buff in set_changes:
            for i in range(1, c_and_r):
                for v_i, directions_buff in zip(vi_c, d_buff):
                    ubication = v_i + orientation * division * i
                    coord_point = round(ubication[coord], self.number_decimals)
                    label = Text(f"{coord_point}",font="Arial",stroke_width=0).scale(self.labels_scale)
                    label.next_to(ubication, directions_buff, buff=self.labels_buff)
                    labels.add(label)

        self.add(grid, axes, labels)

#### Hasta aquí llega el GRID para la clase Bolas

#########################
#### BOLAS / VECINDADES #####
#########################

class  Bolas(Scene):
   
    def construct (self):
        grid = ScreenGrid()
        titulo=TextMobject("Bolas o vecindades")
        text1=TextMobject("Tomemos un punto en el espacio $\\vec{x}_0$")
        text1.move_to((0,3,0))
        text2=TextMobject("Y un radio r>0")
        text2.move_to(text1)
        text3=TextMobject('''Podemos seleccionar los puntos que se encuentran\n
                                a una distancia menor a r de $\\vec{x}_0$''')
        text3.move_to(text1)
        text4=TextMobject('''Esto es conocido como una bola o vecindad''')
        text4.move_to(text1)
        text5=TextMobject("De manera formal definimos bola o vecindad como:")
        text6=TexMobject('B_r(\\vec{x}_0) :=\\lbrace \\vec{x} \\  | \\ d(\\vec{x},\\vec{x}_0)=\\norm{\\vec{x}-\\vec{x}_0}<r \\rbrace')
        text5.move_to(text6.get_center()+UP)
        text7=TextMobject('''Notemos que por lo anterior la bola depende de la norma \n
                            o distancia definida en el espacio''')
        text8=TextMobject('''¿Puedes imaginar como se vería una bola \n
                            con otras normas, por ejemplo con la norma \n
                             infinito o la distancia 1?''')


        r=2 #Se puede modificar para cambiar el radio de la bola
        x0=np.array([0,0,0])   #Se  puede modificar para cambiar el centro de la bola

        punto=Dot()
        puntolabel=TextMobject("$$\\vec{x}_0$$")
        punto.move_to(x0)
        puntolabel.next_to(punto)
        bola = Circle(radius=r,fill_color=GREEN_C,color=GREEN_C,fill_opacity=1)

        self.play(Write(titulo))
        self.wait()
        self.play(FadeOut(titulo))
        self.play(Write(grid)) 
        self.wait()
        self.play(Write(text1))
        self.play(FadeIn(punto),FadeIn(puntolabel))
        self.wait()
        self.play(ReplacementTransform(text1,text2))
        self.wait()
        self.play(ReplacementTransform(text2,text3))
        self.wait()
        self.play(FadeIn(bola))
        self.wait()
        self.play(ReplacementTransform(text3,text4),FadeOut(puntolabel))
        self.wait()
        self.play(FadeOut(bola),FadeOut(grid),FadeOut(text4),FadeOut(punto))
        self.wait()
        self.play(Write(text5))
        self.play(Write(text6))
        self.wait(2)
        self.play(FadeOut(text5),FadeOut(text6))
        self.play(Write(text7))
        self.wait(2)
        self.play(ReplacementTransform(text7,text8))
        self.wait(4)
        self.play(FadeOut(text8))

#########################
#### TIPOS DE PUNTOS #####
#########################

class TiposPuntos(Scene):
    def construct(self):
        interior_t = TextMobject('Punto interior.')
        interior_t.move_to((-3,3.5,0))\
                  .set_color(RED)
        exterior_t = TextMobject('Punto exterior.')
        exterior_t.move_to((-3,2,0))\
                  .set_color(BLUE)
        frontera_t = TextMobject('Punto frontera.')
        frontera_t.move_to((-3,1,0))\
                  .set_color(GREEN)
        interior_def = TexMobject('\\exists r>0, \\ tq. \\ \\mathbb{B}_r(x_0)\\subset A')
        interior_def.move_to((3,3.5,0))\
                    .set_color(RED)
        exterior_def = TexMobject('\\exists r>0, \\ tq. \\ \\mathbb{B}_r(x_0)\\subset A')
        exterior_def.move_to((3,2,0))\
                    .set_color(BLUE)
        frontera_def = TexMobject('''\\forall r>0, \\ tq.''')
        frontera_def_1 = TexMobject('''\\mathbb{B}_r(x_0)\\cap A\\neq \\emptyset''')
        frontera_def_2 = TexMobject('''y''')
        frontera_def_3 = TexMobject('''\\mathbb{B}_r(x_0)\\cap A^c\\neq \\emptyset''')
        frontera_def.move_to((3,1,0))\
                    .set_color(GREEN)
        frontera_def_1.next_to(frontera_def, DOWN, buff = 0.1)\
                      .set_color(GREEN)
        frontera_def_2.next_to(frontera_def_1, DOWN, buff = 0.1)\
                      .set_color(GREEN)
        frontera_def_3.next_to(frontera_def_2, DOWN, buff = 0.1)\
                      .set_color(GREEN)

        texto_1 = TextMobject('Pero, ¿qué significa geométricamente?')

        texto_2 = TextMobject('Demos un conjunto $A$ cualquiera')

        texto_3 = TextMobject('''Por favor regresa el video e intenta \n
                                 asociar las definiciones de cada tipo \n
                                 de punto con el dibujo y visualiza cada \n
                                 definición en este dibujo!''')\
                                     .scale(0.5)\
                                     .move_to((-4.5,2.5,0))
        texto_4 = TextMobject('''El conjunto de todos los puntos \n
                                interiores de un conjunto es el INTERIOR del \n
                                conjunto. ''')\
                                    .set_color(RED)\
                                        .move_to((0,2,0))
        texto_5 = TextMobject('''El conjunto de todos los puntos \n
                                exteriores de un conjunto es el EXTERIOR del \n
                                conjunto. ''')\
                                    .set_color(BLUE)\
                                        .move_to((0,0,0))
        texto_6 = TextMobject('''El conjunto de todos los puntos \n
                                frontera de un conjunto es la FRONTERA del \n
                                conjunto. ''')\
                                    .set_color(GREEN)\
                                        .move_to((0,-2,0))

        texto_7 = TextMobject('''Intenta probar lo siguiente: (Si $A$ es un conjunto) \n
                                 1.- \\ $Int(A)\\cap Fr(A) = \\emptyset$ \n
                                 2.- \\ $Int(A)\\cap Ext(A) = \\emptyset$ \n
                                 3.- \\ $Ext(A)\\cap Fr(A) = \\emptyset$ \n
                                 4.- \\ $Int(A^c) = Ext(A)$''')

        #figs:

        conjunto = Circle(radius = 3, 
                         color = WHITE,
                         fill_color = ORANGE, 
                         fill_opacity=0.5)
        punto_int = Dot(point = (1,1,0))\
            .set_color(RED)
        punto_ext = Dot(point = (3,3,0))\
            .set_color(BLUE)
        punto_fr = Dot(point = (1.5, np.sqrt(9-1.5**2), 0))\
            .set_color(GREEN)

        flecha_int = Arrow((-1.5,3.5,0),(0.3,3.5,0))\
                    .set_color(RED)
        flecha_ext = Arrow((-1.5,2,0),(0.3,2,0))\
                    .set_color(BLUE) 
        flecha_fr = Arrow((-1.5,1,0),(1.5,1,0))\
                    .set_color(GREEN)

        cjto_int = Circle(radius = 1,
                          color = RED,
                          fill_color = RED,
                          fill_opacity = 0.7)\
                              .move_to((1,1,0))
        cjto_ext = Circle(radius = 0.5,
                          color = BLUE,
                          fill_color = BLUE,
                          fill_opacity = 0.7)\
                              .move_to((3,3,0))
        cjto_fr = Circle(radius = 0.5,
                          color = GREEN,
                          fill_color = GREEN,
                          fill_opacity = 0.7)\
                              .move_to(punto_fr.get_center())
        #GPOS

        gpo_1 = VGroup(interior_t, exterior_t, frontera_t, interior_def, exterior_def, frontera_def, flecha_int, flecha_ext, flecha_fr,
                        frontera_def_1, frontera_def_2, frontera_def_3)

        # Secuencia de la animación
        #self.play(Write(gpo_1))
        #self.wait(5)
        #self.play(ReplacementTransform(gpo_1, texto_1))
        #self.wait(3)
        #self.play(ReplacementTransform(texto_1,texto_2))
        #self.wait(3)
        self.play(ReplacementTransform(texto_2, conjunto))
        self.wait(3)
        self.play(Write(punto_int), Write(punto_ext), Write(punto_fr))
        self.wait(3)
        self.play(DrawBorderThenFill(cjto_int),
                  DrawBorderThenFill(cjto_ext),
                  DrawBorderThenFill(cjto_fr))
        self.play(Write(texto_3))
        self.wait(3)
        self.play(FadeOut(texto_3), 
                  FadeOut(cjto_int),
                  FadeOut(cjto_ext),
                  FadeOut(cjto_fr),
                  FadeOut(conjunto),
                  FadeOut(punto_int),
                  FadeOut(punto_ext),
                  FadeOut(punto_fr))
        self.play(Write(texto_4),Write(texto_5),Write(texto_6))
        self.wait(10)
        self.play(FadeOut(texto_4),FadeOut(texto_5),FadeOut(texto_6))
        self.play(Write(texto_7))

#########################
#### CONJUNTOS ABIERTOS #####
#########################

class Conjuntos_abiertos (Scene):
    def construct (self):
        titulo=TextMobject("Conjuntos abiertos")
        text1=TextMobject("Veamos el siguiente conjunto")
        text1.move_to(3*UP)
        text2=TextMobject("A")
        text2.move_to(text1.get_center()+0.8*DOWN)
        text2.set_color(PURPLE)
        text3=TextMobject('''Notemos que al tomar un punto en la orilla azul \n
                            se puede dibujar una bola con centro en ese punto''')
        text3.move_to(text1.get_center()+0.3*DOWN)
        text3_1=TextMobject('''Y con cualquier radio, la bola intersecta el \n
                                conjunto y el exterior de este ''')
        text3_1.move_to(text3)
        text4=TextMobject('''Con esto se puede observar que los puntos de color azul \n
                            representan la frontera de A''')
        text4.move_to(text3.get_center())
        text5=TextMobject('''Sin embargo ningún elemento de la frontera de A \n
                             está contenido en A \n''')
        text5.move_to(text4.get_center())
        def1=TextMobject('''A los conjuntos que cumplen lo anterior \n
                            los conocemos como ABIERTOS''')
        def2=TextMobject("En otras palabras, un conjunto A es abierto si: $$Fr(A) \\cap A=\\emptyset $$")
        
        creature = SVGMobject('Topologia_SVGs/abierto.svg',fill_color=PURPLE,color=BLACK)
        creature.move_to(DOWN)
        creature.scale(3)
        creature1=SVGMobject('Topologia_SVGs/abierto.svg',fill_color=PURPLE,color=BLUE_C)
        creature1.move_to(DOWN)
        creature1.scale(3)
        creature2=creature.copy()

        punto1=Dot(color=BLUE_C)
        punto1.next_to(creature,RIGHT,buff=1)
        circulo1 = Circle(color=RED, radius=1)
        circulo1.move_to(punto1)
        circulo1_1 = Circle(color=RED, radius=0.5)
        circulo1_1.move_to(punto1)

        punto2=Dot(color=BLUE_C)
        punto2.next_to(creature,UP,buff=-0.15)
        circulo2 = Circle(color=RED, radius=1)
        circulo2.move_to(punto2)
        circulo2_1=Circle(color=RED, radius=2)
        circulo2_1.move_to(punto2)

        # Secuencia de la animación
        self.play(Write(titulo))
        self.wait()
        self.play(FadeOut(titulo))
        self.wait()
        self.play(Write(text1))
        self.play(Write(text2))
        self.wait()
        self.play(SpinInFromNothing(creature))
        self.wait(1)
        self.play(FadeOut(text1),FadeOut(text2))
        self.play(Write(text3),ReplacementTransform(creature,creature1))
        self.wait()
        self.play(FadeIn(punto1),FadeIn(circulo1))
        self.wait()
        self.play(ReplacementTransform(text3,text3_1))
        self.wait()
        self.play(ReplacementTransform(circulo1,circulo1_1))
        self.wait()
        self.play(FadeOut(punto1),FadeOut(circulo1_1))
        self.play(FadeIn(punto2),FadeIn(circulo2))
        self.wait()
        self.play(ReplacementTransform(circulo2,circulo2_1))
        self.play(FadeOut(punto2),FadeOut(circulo2_1))
        self.play(FadeOut(text3_1))
        self.play(Write(text4))
        self.wait(3)
        self.play(ReplacementTransform(text4,text5),
                  ReplacementTransform(creature1,creature2))
        self.wait(2)
        self.play(FadeOut(creature2))
        #self.play(ReplacementTransform(text5,def1))
        self.play(Write(def1))
        self.wait(3)
        self.play(FadeOut(def1),FadeOut(text5))
        self.play(Write(def2))
        self.wait(2)
        self.play(FadeOut(def2))
        self.wait()

        #Segunda caracterizacion
        titulo1=TextMobject('''Segunda caracterización de conjuntos \n
                              abiertos''')
        text7=TextMobject('''Consideremos el mismo conjunto''')
        text7.move_to(3*UP)
        text7_1=TextMobject("A")
        text7_1.move_to(text1.get_center()+0.8*DOWN)
        text7_1.set_color(PURPLE)
        text8=TextMobject('''Notemos que al tomar cualquier punto \n
                            en A, este es un punto interior''')
        text8.move_to(text1)
        text9=TextMobject('''Por lo cual todos los puntos de A \n
                            son puntos interiores''')
        text9.move_to(text1)
        text10=TextMobject('''Entonces un conjunto es abierto si \n
                            todos sus puntos son interiores''')
        text11=TextMobject('''De manera más formal''')
        text11_1=text11.copy()
        text11_1.move_to(2*UP)
        text12=TextMobject('''Un conjunto A es abierto si:$$\\forall x\\in A$$
                                x es punto interior''')

        creature3 = SVGMobject('Topologia_SVGs/abierto.svg',fill_color=PURPLE, 
        fill_opacity=1,color=BLACK)
        creature3.move_to(DOWN)
        creature3.scale(3)
        punto3=Dot(color=PURPLE_E)
        punto3.move_to(creature3.get_center()+0.5*RIGHT)
        circulo3 = Circle(color=RED, radius=0.5)
        circulo3.move_to(punto3)

        punto4=Dot(color=PURPLE_E)
        punto4.move_to(creature3.get_center()+1.5*RIGHT+2*UP)
        circulo4 = Circle(color=RED, radius=0.15)
        circulo4.move_to(punto4)

        punto5=Dot(color=PURPLE_E)
        punto5.move_to(creature3.get_center()+1.9*LEFT+1.41*DOWN)
        circulo5 = Circle(color=RED, radius=0.12)
        circulo5.move_to(punto5)
        

        # Secuencia de la animación
        self.play(Write(titulo1))
        self.wait()  
        self.play(FadeOut(titulo1))
        self.play(Write(text7))
        self.play(Write(text7_1))
        self.play(GrowFromCenter(creature3))
        self.wait()
        self.play(ReplacementTransform(text7,text8),FadeOut(text7_1))
        self.play(FadeIn(punto3),FadeIn(circulo3))
        self.wait()
        self.play(ReplacementTransform(punto3,punto4),
        ReplacementTransform(circulo3,circulo4))
        self.wait()
        self.play(ReplacementTransform(punto4,punto5),
        ReplacementTransform(circulo4,circulo5))
        self.wait()
        self.play(FadeOut(punto5),FadeOut(circulo5))
        self.play(ReplacementTransform(text8,text9))
        self.wait()
        self.play(FadeOut(creature3),FadeOut(text9))
        self.play(Write(text10))
        self.wait()
        self.play(ReplacementTransform(text10,text11))
        self.wait()
        self.play(ReplacementTransform(text11,text11_1))
        self.wait()
        self.play(Write(text12))
        self.wait()

#########################
#### CONJUNTOS CERRADOS #####
#########################

class Conjuntos_cerrados (Scene):
    def construct(self):
        titulo=TextMobject("Conjuntos cerrados")
        text1=TextMobject("Consideremos el siguiente conjunto")
        text1.move_to(3*UP)
        text1_1=TextMobject("B")
        text1_1.move_to(text1.get_center()+0.8*DOWN)
        text1_1.set_color(BLUE_B)
        text2=TextMobject('''Podemos tomar un punto de la "orilla"  \n
                             y dibujar alrededor de el una bola''')

        text2.move_to(2.5*UP)
        text3=TextMobject('''y sin importar el radio de la bola \n
                            esta intersecta a B y el exterior de B''')
        text3.move_to(text2)
        text4=TextMobject('''Por lo cual la orilla que se marca en rojo es la frontera \n
                            del conjunto B''')
        text4.move_to(text1)
        text5=TextMobject('''Con esto nos damos cuenta que la frontera del conjunto está \n
                              cotenida en el conjunto''')
        text5.move_to(text1)
        text6=TextMobject('''A los conjuntos que cumplen lo anterior se les conoce \n
                            como conjuntos CERRADOS''')
        def1=TextMobject(''' Más formalmente:\n
                             un conjunto A es cerrado si:\n
                            $$Fr(A)\\subset A$$''')
        def1.move_to(UP)

        cerrado=SVGMobject('Topologia_SVGs/cerrado.svg',color=WHITE,fill_color=BLUE_B)
        cerrado.move_to(DOWN)
        cerrado.scale(3)
        cerrado1=cerrado.copy()
        cerrado1.set_stroke(RED)
        cerrado2=SVGMobject('Topologia_SVGs/cerrado.svg',color=WHITE,fill_color=BLUE_B)
        cerrado2.move_to(DOWN)
        cerrado2.scale(3)

        punto1=Dot()
        punto1.next_to(cerrado,LEFT,buff=-0.22)
        circulo1 = Circle(color=RED, radius=0.5)
        circulo1.move_to(punto1)
        circulo1_1 = Circle(color=RED, radius=2)
        circulo1_1.move_to(punto1)

        punto2=Dot()
        punto2.next_to(cerrado,UP+RIGHT,buff=-0.1)
        circulo2 = Circle(color=RED, radius=1)
        circulo2.move_to(punto2)
        circulo2_1=Circle(color=RED, radius=0.4)
        circulo2_1.move_to(punto2)

        # Secuencia de la animación
        self.play(Write(titulo))
        self.wait()
        self.play(FadeOut(titulo))
        self.play(Write(text1))
        self.play(Write(text1_1))
        self.wait()
        self.play(SpinInFromNothing(cerrado))
        self.wait()
        self.play(ReplacementTransform(text1,text2),FadeOut(text1_1))
        self.play(FadeIn(punto1))
        self.play(FadeIn(circulo1))
        self.wait()
        self.play(ReplacementTransform(circulo1,circulo1_1))
        self.wait()
        self.play(ReplacementTransform(text2,text3))
        self.play(FadeOut(circulo1_1),FadeOut(punto1))
        self.play(ReplacementTransform(punto1,punto2),ReplacementTransform(circulo1_1,circulo2))
        self.play(ReplacementTransform(circulo2,circulo2_1))
        self.wait()
        self.play(FadeOut(circulo2_1),FadeOut(punto2))
        self.wait()
        self.play(ReplacementTransform(cerrado,cerrado1),ReplacementTransform(text2,text3))
        self.play(ReplacementTransform(text3,text4))
        self.wait()
        self.play(ReplacementTransform(cerrado,cerrado1))
        self.wait(2)
        self.play(ReplacementTransform(cerrado1,cerrado2))
        self.play(ReplacementTransform(text4,text5))
        self.wait(2)
        self.play(FadeOut(cerrado2))
        self.wait()
        self.play(Write(text6))
        self.wait()
        self.play(FadeOut(text5),FadeOut(text6))
        self.wait()
        self.play(Write(def1))
        self.wait(2)
        self.play(FadeOut(def1))
        self.wait()

        #Segunda caracterizacion

        titulo2=TextMobject('''Segunda caracterización de \n
                            conjuntos cerrados''')
        text7=TextMobject('''Tomemos el mismo conjunto''')
        text7.move_to(3*UP)
        text7_1=TextMobject("B")
        text7_1.move_to(text7.get_center()+0.8*DOWN)
        text7_1.set_color(BLUE_B)
        text8=TextMobject('''Notemos que al tomar cualquier punto \n
                            que no este contenido en B''')
        text8.move_to(text7)
        text9=TextMobject('''Podemos dibujar alrededor de una bola \n
                                y esta queda contenida en Ext(B)''')
        text9.move_to(text7)
        #text10=TextMobject('''Y queda contenida en Ext(B)''')
        #text10.move_to(text7)
        text11=TextMobject('''Por lo cual Ext(B) es abierto''')
        text11.move_to(text7)
        text12=TextMobject('''Entonces un cerrado B también \n
                                cumple que: \n
                                Ext(B) es abierto''')
        pregunta=TextMobject('''¿Consideras que se pueden clasificar los\n
                                    conjuntos en solo cerrados y abiertos?''')

        cerrado3=SVGMobject('Topologia_SVGs/cerrado.svg',color=WHITE,fill_color=BLUE_B)
        cerrado3.move_to(DOWN)
        cerrado3.scale(3)

        punto3=Dot(color=RED)
        punto3.move_to(cerrado3.get_center()+LEFT+2*DOWN)
        circulo3 = Circle(color=RED, radius=0.8)
        circulo3.move_to(punto3)
    

        punto4=Dot(color=RED)
        punto4.move_to(cerrado3.get_center()+1.5*RIGHT+2*UP)
        circulo4 = Circle(color=RED, radius=0.24)
        circulo4.move_to(punto4)
      


        # Secuenca de la animación
        self.play(Write(titulo2))
        self.wait()
        self.play(FadeOut(titulo2))
        self.play(Write(text7))
        self.play(Write(text7_1))
        self.play(DrawBorderThenFill(cerrado3))
        self.wait()
        self.play(ReplacementTransform(text7,text8),FadeOut(text7_1))
        self.wait()
        self.play(FadeIn(punto3))
        self.play(ReplacementTransform(text8,text9),FadeIn(circulo3))
        self.wait()
        self.play(ReplacementTransform(punto3,punto4),ReplacementTransform(circulo3,circulo4))
        self.wait()
        self.play(ReplacementTransform(text9,text11),FadeOut(punto4),FadeOut(circulo4))
        self.wait()
        self.play(FadeOut(text11),FadeOut(cerrado3))
        self.play(Write(text12))
        self.wait()
        self.play(ReplacementTransform(text12,pregunta))
        self.wait(2)

#########################
#### OBS CERRADOS/ABIERTOS #####
#########################
        
class ObservacionCerradosAbiertos(Scene):
    def construct(self):
        
        titulo=TextMobject('''Observación de conjuntos\n
                             abiertos y cerrados ''')

        #OBSERVACION
        text1=TextMobject('''Consideremos el siguiente conjunto''')
        text1.move_to(3*UP)
        text1_1=TextMobject("A")
        text1_1.set_color(BLUE_E)
        text1_1.move_to(text1.get_center()+0.8*DOWN)
        text2=TextMobject('''Notemos que los puntos en rojo son parte de \n
                            la frontera de A''')
        text2.move_to(text1)
        text3=TextMobject('''Sin embargo no están contenidos en el conjunto ''')
        text3.move_to(text1.get_center()+0.8*DOWN)
        text3_1=TextMobject(''' Por lo cual: $$Fr(A) \\not\\subset A$$''')
        text3_1.move_to(text1)
        text4=TextMobject("Lo que implica que A no es cerrado")
        text4.move_to(text1.get_center()+0.8*DOWN)
        text5=TextMobject('''Además los puntos en blanco también pertenecen\n
                             a la frontera de A''')
        text5.move_to(text1.get_center()+0.8*DOWN)
        text5_1=TextMobject('''$$\\implies Fr(A)\cap A\\neq\\emptyset $$''')
        text5_1.move_to(text1)
        text6=TextMobject('''Por lo cual A no es cerrado ni abierto''')
        text6.move_to(text1.get_center()+0.8*DOWN)
        text7=TextMobject('''Esto nos induce a que porque un conjunto no sea\n
                            cerrado no implica que sea abierto y viceversa''')

        pregunta=TextMobject('''Ahora que sabes más de los conjuntos abiertos \n
                                y cerrados, ¿puedes responder lo siguiente? \n
                                Sea A un conjunto:''')
        pregunta_1=pregunta.copy()
        pregunta_1.move_to(text1)
        pregunta1=TextMobject('''¿Int(A) es abierto o cerrado?''')
        pregunta2=TextMobject('''¿Fr(A) es abierto o cerrado?''')
        pregunta3=TextMobject('''¿$B_r(x_0)$ es abierta o cerrada?''')
        

        obs1 = SVGMobject('Topologia_SVGs/observacion1.svg')
        obs1.move_to(1*DOWN)
        obs1.scale(2.5)
        obs1[0:1].set_color(BLUE_E)
        obs1[0:1].set_stroke(BLUE_E)
        obs1[1:2].set_color(BLUE_E)
        obs1[1:2].set_stroke(WHITE)
        obs1[2:3].set_stroke(WHITE)
        obs1[2:3].set_color(BLUE_E)


        obs1_1 = obs1.copy()
        obs1_1.move_to(1*DOWN)
        obs1_1[0:1].set_color(BLUE_E)
        obs1_1[0:1].set_stroke(RED)
        obs1_1[1:2].set_color(BLUE_E)
        obs1_1[1:2].set_stroke(WHITE)
        obs1[2:3].set_stroke(BLUE_E)
        obs1[2:3].set_color(BLUE_E)

        obs1_2 = SVGMobject('Topologia_SVGs/observacion1.svg')
        obs1_2.move_to(1*DOWN)
        obs1_2.scale(2.5)
        obs1_2[0:1].set_color(BLUE_E)
        obs1_2[0:1].set_stroke(BLUE_E)
        obs1_2[1:2].set_color(BLUE_E)
        obs1_2[1:2].set_stroke(WHITE)
        obs1_2[2:3].set_stroke(BLUE_E)
        obs1_2[2:3].set_color(BLUE_E)

        obs1_3=obs1.copy()


        # Secuencia de la animación
        self.play(Write(titulo))
        self.wait()
        self.play(FadeOut(titulo))
        self.play(Write(text1))
        self.play(Write(text1_1))
        self.play(SpinInFromNothing(obs1))
        self.wait(2)
        self.play(ReplacementTransform(text1,text2),FadeOut(text1_1),ReplacementTransform(obs1,obs1_1))
        self.wait(2)
        self.play(ReplacementTransform(text2,text3))
        self.play(ReplacementTransform(obs1_1,obs1_2))
        self.wait(2)
        self.play(ReplacementTransform(text3,text3_1))
        self.wait(2)
        self.play(ReplacementTransform(text3_1,text4))
        self.wait(2)
        self.play(ReplacementTransform(obs1_2,obs1_3))
        self.play(ReplacementTransform(text4,text5))
        self.wait(2)
        self.play(ReplacementTransform(text5,text5_1))
        self.wait()
        self.play(ReplacementTransform(text5_1,text6))
        self.wait(2)
        self.play(FadeOut(text6),ShrinkToCenter(obs1_3))
        self.play(Write(text7))
        self.wait(2)
        self.play(FadeOut(text7))
        self.play(Write(pregunta))
        self.wait()
        self.play(ReplacementTransform(pregunta,pregunta_1))
        self.play(Write(pregunta1))
        self.wait()
        self.play(ReplacementTransform(pregunta1,pregunta2))
        self.wait()
        self.play(ReplacementTransform(pregunta2,pregunta3))
        self.wait()
        self.play(FadeOut(pregunta3),FadeOut(pregunta_1))

#########################
#### CERRADURA #####
#########################

class Cerradura(Scene):
    def construct(self):
        title = TextMobject('''Cerradura''')
        defi = TextMobject('''Definimos la cerradura de un conjunto''',''' $A$''',''' como \n
                            $\\bar{A}=cl(A):=$''','''$A$''','''$\\cup$''','''$Fr(A)$''')
        defi.set_color_by_tex_to_color_map({
            '''$A$''': YELLOW,
            '''Fr(A)''': RED
        })

        conjuntoA = SVGMobject("Topologia_SVGs/cjtoA.svg",color=RED,fill_color=YELLOW,fill_opacity=1.2).scale(2)
        nameA = TexMobject("A").next_to(conjuntoA,DOWN)
        note = TextMobject('''*Recuerda que el conjunto puede contener elementos de su frontera, es decir, \n
                            el conjunto no es necesariamente igual a su interior''').scale(0.55).to_edge(DOWN)
        group = VGroup(conjuntoA,defi,nameA,note)

        text1 = TextMobject('''Veamos algunas propiedades sobre la cerradura''')
        text2 = TexMobject(r"cl(A\cup B)",r"=",r"cl(A)",r"\cup",r"cl(B)")
        text2.set_color_by_tex_to_color_map({
            "cl(A)": YELLOW,
            "cl(B)": BLUE
        })

        conjuntoB = SVGMobject("Topologia_SVGs/cjtoB.svg",color=BLUE,fill_color=BLUE).shift(2.5*RIGHT).scale(2)
        conjuntoA.set_color(YELLOW).shift(2.5*LEFT)
        A = TexMobject("A").next_to(conjuntoA,DOWN)
        B = TexMobject("B").next_to(conjuntoB,DOWN)
        names = VGroup(A,B)
        conjuntos = VGroup(conjuntoA,conjuntoB)
        conjuntoA2 = SVGMobject("Topologia_SVGs/cjtoA.svg",color=WHITE,fill_color=WHITE).shift(2.5*LEFT).scale(2)
        conjuntoB2 = SVGMobject("Topologia_SVGs/cjtoB.svg",color=WHITE,fill_color=WHITE).shift(2.5*RIGHT).scale(2)
        conjuntos2 = VGroup(conjuntoA2,conjuntoB2)

        text3 = TextMobject('''Intenta demostrar que''')
        prop1 = TexMobject(r"x\in cl(A) \Leftrightarrow \forall \varepsilon>0,\ B_{\varepsilon}\cap A\neq\emptyset").next_to(text3,DOWN)
        
        #Secuencia de la animación
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title),run_time=0.5)
        self.play(Write(defi))
        self.wait()
        self.play(ApplyMethod(defi.to_edge,UP))
        #
        self.play(DrawBorderThenFill(conjuntoA),rate_func=linear)
        self.play(Write(nameA),Write(note))
        self.wait(4)
        self.play(FadeOut(group))
        #
        self.play(Write(text1))
        self.wait(2)
        self.play(ReplacementTransform(text1,text2))
        self.play(ApplyMethod(text2.to_edge,UP))
        self.play(DrawBorderThenFill(conjuntos2),Write(names))
        self.wait()
        self.play(ReplacementTransform(conjuntos2,conjuntos))
        self.wait()
        self.play(FadeOut(conjuntos),FadeOut(text2),FadeOut(names))
        #
        self.play(Write(text3))
        self.play(Write(prop1))
        self.wait(2)
        self.play(FadeOut(text3),FadeOut(prop1))

###################################
#### PUNTOS AISLADOS/ACUMULACION #####
###################################

class Puntos_Aislado_y_Acumulacion(Scene):
    def construct(self):
        title = TextMobject('''Puntos aislados y \n
                            puntos de acumulación''')
        text1 = TextMobject('''Considera el siguiente conjunto ''','''$A$''')
        text1.set_color_by_tex_to_color_map({
            "A": YELLOW
        })
        text2 = TextMobject('''Fíjate en los puntos ''','''$x$''',''' e ''','''$y$''').to_edge(UP)
        text2.set_color_by_tex_to_color_map({
            "x": RED,
            "y": BLUE
        })
        B = SVGMobject("Topologia_SVGs/cjtoA.svg",color=YELLOW,fill_color=YELLOW).shift(1.5*LEFT).scale(2)
        x = Dot(point=((1,0,0)),color=YELLOW,radius=0.1)
        x_label = TexMobject("x",color=RED).next_to(x,DOWN)
        cjto = VGroup(B,x)
        y = Dot(point=((-1.8,0.5,0)),color=BLUE,radius=0.1)
        y_label = TexMobject("y",color=BLUE).next_to(y,DOWN)
        grupo = VGroup(y,x_label,y_label)
        bola = Circle(radius=1,color=WHITE).move_to((1,0,0))
        radio = Line(((1,0,0)),((2,0,0)),color=WHITE)
        eps = TexMobject(r"\varepsilon").next_to(radio,UP)
        aislado = VGroup(bola,radio,eps)
        
        text3 = TextMobject('''¿Cuál crees que sea un punto aislado?''').to_edge(UP)
        text4 = TextMobject('''¿Cuál crees que sea un punto de acumulación?''').to_edge(UP)
        text5 = TextMobject('''$x$ es un punto aislado, al tomar alguna $\\varepsilon >0$ \n
                             vemos que $B_{\\varepsilon}(x)\\cap A=\\{x\\}$''').to_edge(UP)
        
        text6 = TextMobject('''Mientras que $y$ es un punto de acumulación pues $\\forall\\varepsilon >0$ \n
                            se cumple que $(B_{\\varepsilon}(y)\\backslash\\{y\\})\\cap A\\neq \\emptyset$''').to_edge(UP)

        
        text7 = TextMobject('''El conjunto de todos los puntos de acumulación de $A$ se llama \n
                            conjunto derivado, y se denota por $der(A)$''')
        text8 = TextMobject('''Intenta demostrar las siguientes propiedades de dicho conjunto:''').move_to((0,2.5,0))
        prop1 = TextMobject('''$der(A)$ es la unión de $int(A)$ y los puntos frontera no aislados''').move_to((0,1,0))
        prop2 = TexMobject(r"cl(A)=A\cup der(A)").next_to(prop1,DOWN)
        prop3 = TextMobject('''Todos los puntos de $int(A)$ son de acumulación''').next_to(prop2,DOWN)
        prop4 = TextMobject('''Todos los puntos aislados de $A$ son puntos frontera de $A$''').next_to(prop3,DOWN)
        propiedades = VGroup(text8,prop1,prop2,prop3,prop4)

        #Secuencia de la animación
        self.play(Write(title))
        self.wait()
        self.play(ReplacementTransform(title,text1))
        self.play(ApplyMethod(text1.to_edge,UP))
        self.play(DrawBorderThenFill(cjto))
        self.wait()
        self.play(ReplacementTransform(text1,text2),ApplyMethod(x.set_color,RED),Write(grupo))
        self.wait(2)
        #
        self.play(ReplacementTransform(text2,text3))
        self.wait(2)
        self.play(ReplacementTransform(text3,text4))
        self.wait(2)
        self.play(ReplacementTransform(text4,text5),ShowCreation(aislado))
        self.wait(3)
        self.play(ReplacementTransform(text5,text6),FadeOut(aislado))
        ##
        i=4
        bola_ant = Circle(radius=i,color=GREEN).move_to((-1.8,0.5,0))
        while i>0.2:
            bola_sig = Circle(radius=i,color=GREEN).move_to((-1.8,0.5,0))

            self.play(ReplacementTransform(bola_ant,bola_sig))
            self.wait()
            
            bola_ant = bola_sig
            i=0.5*i
        
        self.play(FadeOut(text6),FadeOut(bola_ant),FadeOut(cjto),FadeOut(grupo))
        ##
        self.play(Write(text7))
        self.wait(3)
        self.play(ReplacementTransform(text7,text8))
        self.wait()
        self.play(Write(prop1))
        self.play(Write(prop2))
        self.play(Write(prop3))
        self.play(Write(prop4))
        self.wait(2)
        self.play(FadeOut(propiedades))

########################
#### CUBIERTAS     #####
########################

class Cubierta(Scene):
    def construct(self):
        grid = ScreenGrid()

        ###Texto
        t_1 = TextMobject('Sea $A \\subset \\mathbb{R}^n$')
        t_2 = TextMobject('Definimos una cubierta de $ A $')
        t_3 = TextMobject('como una colección de subconjuntos $\\mathcal{F} \\subset \\mathbb{R}^n$')    
        t_4 = TextMobject('tal que $A \\subseteq \\bigcup_{U \\subset \\mathcal{F}} U$')
        t_5 = TextMobject('Por ejemplo, sea $A$  el siguiente conjunto:').move_to(3*UP)
        t_6 = TextMobject('Entonces una posible cubierta $\\mathcal{F}$ podría ser: ').move_to(3*UP)
        t_7 = TextMobject('Una cubierta puede ser abierta o cerrada').move_to(3*UP)
        t_8 = TextMobject('dependiendo de si los subconjuntos $U_{i}$ que la componen').move_to(3*UP)
        t_9 = TextMobject('son abiertos').move_to(3*UP)
        t_10 = TextMobject('o cerrados').move_to(3*UP)
        t_11 = TextMobject('Observemos que en este caso los conjuntos $U_{i}$ se sobreponen').move_to(3*UP)
        t_12 = TextMobject('por lo que el conjunto $A$ queda totalmente cubierto').move_to(3*UP)
        t_13 = TextMobject('independientemente de que $\\mathcal{F}$ sea abierta o cerrada').move_to(3*UP)
        t_14 = TextMobject('¿Es posible definir una cubierta abierta tipo rompecabezas?').move_to(3*UP)
        t_15 = TextMobject('¿Qué papel jugaría $Fr(U_{i})$ en este tipo de cubierta?').move_to(3*UP)


        ###Conjunto y cubiertas
        Conjunto_Cubierto = SVGMobject("Topologia_SVGs/Cubierta.svg").scale(2)
        A = Conjunto_Cubierto[0].set_color(BLUE).next_to(t_5, 5*DOWN)
        cover_1 = Conjunto_Cubierto[1:6].next_to(t_6, 2*DOWN)
        index = VGroup()
        colors = it.cycle([YELLOW,GREEN,PURPLE,PINK,RED,TEAL])
        for i in range(len(cover_1)):
            text= TextMobject('$U_{%d}$'%(i+1))
            color = next(colors)
            cover_1[i].set_fill(color, opacity=0.4).set_stroke(color,0.5)
            text.move_to(cover_1[i])
            index.add(text)
        cover_2 = Conjunto_Cubierto[6:11].next_to(t_12, 2*DOWN)
        for i in range(len(cover_2)):
            color = next(colors)
            cover_2[i].set_fill(color, opacity=0.4).set_stroke(color,0.5)

        ###Grupos
        Group_1 = VGroup(t_5, A)
        Group_2 = VGroup(t_6, A)
        Group_3 = VGroup(cover_1, index)
        Group_4 = VGroup(t_15, cover_2, A)

        # Secuencia de la animación
        self.play(Write(t_1))
        self.wait(2)
        self.play(ReplacementTransform(t_1, t_2))
        self.wait(2)
        self.play(ReplacementTransform(t_2, t_3))
        self.wait(2)
        self.play(ReplacementTransform(t_3, t_4))
        self.wait(2)
        self.play(ReplacementTransform(t_4, Group_1))
        self.wait(2)
        self.play(ReplacementTransform(Group_1, Group_2))
        self.play(FadeIn(Group_3))
        self.wait(2)
        self.play(ReplacementTransform(t_6, t_7))
        self.wait(2)
        self.play(ReplacementTransform(t_7, t_8))
        self.wait(2)
        self.play(ReplacementTransform(t_8, t_9))
        self.wait(2)
        self.play(ReplacementTransform(t_9, t_10))
        self.remove(Group_3).add(cover_1.set_stroke(WHITE, 3))
        self.wait(2)
        self.play(ReplacementTransform(t_10, t_11))
        self.wait(2)
        self.play(ReplacementTransform(t_11, t_12))
        self.wait(2)
        self.play(ReplacementTransform(t_12, t_13))
        self.wait(2)
        self.play(ReplacementTransform(t_13, t_14))
        self.play(ReplacementTransform(cover_1.set_stroke(WHITE, 3), cover_2))
        self.wait(2)
        self.play(ReplacementTransform(t_14, t_15))
        self.wait(2)
        self.play(FadeOut(Group_4))

########################
#### NUM LEBESGUE  #####
########################

class NumLebesgue(Scene):
    def construct(self):
        grid = ScreenGrid()
        ###Texto
        titulo = TextMobject('Lema del Número de Lebesgue')
        t_1 = TextMobject('Sean $(X, d)$ un espacio metrico completo').move_to(3*UP)
        t_2 = TextMobject('y $\\mathcal{F}$ una cubierta abierta de $X$').move_to(3*UP)
        t_3 = TextMobject('$\\implies \\exists$ $\\epsilon > 0$').move_to(3*UP)
        t_4 = TextMobject('tal que $\\forall$ $x \in X$').move_to(3*UP)
        t_5 = TextMobject('$\\exists$ $U \\in \\mathcal{F}$').move_to(3*UP)
        t_6 = TextMobject('tal que $B(x, \\epsilon) \\subseteq U$').move_to(3*UP)
        t_7 = TextMobject('¿Puedes probarlo formalmente?')

        ###Dibujos

        Conjunto_Cubierto = SVGMobject("Topologia_SVGs/Lebesgue.svg").scale(2)
        X = Conjunto_Cubierto[0].set_color(GREEN).next_to(t_1, 5*DOWN)
        cover = Conjunto_Cubierto[1:7].next_to(t_2, 2*DOWN)
        colors = it.cycle([YELLOW,RED,PURPLE,PINK,BLUE,TEAL,WHITE])
        for i in range(len(cover)):
            color = next(colors)
            cover[i].set_fill(color, opacity=0.4).set_stroke(color,0.5)
        line=Line(np.array([1,0,0]),np.array([1.51,0,0])).move_to((1, -0.8, 0))
        brace = Brace(line, UP)
        epsilon = TextMobject('$\\epsilon$').next_to(brace, UP)
        dot = Dot((0,0,0), color = WHITE, radius = 0.05).move_to(line, LEFT)
        x = TextMobject('$x$').next_to(dot, LEFT)
        U = TextMobject('$U$').next_to(cover[5], RIGHT)
        circle = Circle(radius=0.49,fill_color=RED,color=RED,fill_opacity=0.8).move_to(dot)

        ###Grupos
        Group_1 = VGroup(t_1, X)
        Group_2 = VGroup(line, brace, epsilon)
        Group_3 = VGroup(dot, x)
        Group_4 = VGroup(line, brace, epsilon, dot, x)
        Group_5 = VGroup(line, brace, epsilon, dot, x, cover, X, t_6, circle, U)

        # Secuencia de la animación
        self.play(Write(titulo))
        self.wait(2)
        self.play(ReplacementTransform(titulo, Group_1))
        self.wait(2)
        self.play(ReplacementTransform(t_1, t_2))
        self.play(FadeIn(cover))
        self.wait(2)
        self.play(ReplacementTransform(t_2,t_3))
        self.play(FadeIn(Group_2))
        self.play(FadeOut(brace))
        self.play(FadeOut(epsilon))
        self.add(Group_3)
        self.play(ReplacementTransform(t_3, t_4))
        self.wait(2)
        self.play(FadeOut(x))
        self.play(ReplacementTransform(t_4, t_5))
        self.play(DrawBorderThenFill(cover[5].set_stroke(WHITE, 1)))
        self.add(U)
        self.wait(2)
        self.play(ReplacementTransform(t_5, t_6))
        self.play(DrawBorderThenFill(circle))
        self.play(FadeIn(Group_4))
        self.wait(2)
        self.play(ReplacementTransform(Group_5, t_7))
        self.wait(2)
        self.play(FadeOut(t_7))

#############################
#### DISCONEXOS/CONEXOS #####
#############################

class ConjuntosConexos(Scene):
    def construct(self):
        # Título y texto
        titulo = TextMobject("Disconexidad y conexidad")
        intui = TextMobject("De forma intuitiva, un conjunto"," disconexo" ," es aquel")
        intui[1].set_color(RED)
        tivo = TextMobject("compuesto por dos o más partes", " separadas").next_to(intui,DOWN)
        tivo[1].set_color(RED)
        intuitivo = VGroup(intui, tivo)
        tdisconexo_a = TextMobject("Formalmente un conjunto es", " disconexo", " si y sólo si")
        tdisconexo_a[1].set_color(RED)
        tdisconexo_b = TextMobject("satisface tres propiedades con respecto a otros conjuntos").next_to(tdisconexo_a,DOWN)
        tdisconexo = VGroup(tdisconexo_a,tdisconexo_b)
        
        #Conjunto disconexo
        el_disconexo = TextMobject(" A", " es un conjunto disconexo si y sólo si ").to_edge(UP)
        el_disconexo[0].set_color(RED)
        disconexo = SVGMobject("Topologia_SVGs/disconexo.svg", fill_color= RED, fill_opacity=1,stroke_opacity = 0).shift(3*LEFT)
        disconexo_label = TextMobject("A").next_to(disconexo.get_center(),5*DOWN)
        gdisconexo = VGroup(disconexo, disconexo_label)
    
        #Conjuntos abiertos
        abiertos = TextMobject("Existen ", "U", " y" , " V", " abiertos tales que:").scale(0.9).shift(2*UP+3*RIGHT)
        abiertos[1].set_color(ORANGE)
        abiertos[3].set_color(YELLOW)
        cjtoU_set = Circle(radius = 1.5, fill_opacity = 0.6, stroke_opacity = 0).shift(4.2*LEFT).set_color(ORANGE)
        cjtoU_label = TextMobject("U").next_to(cjtoU_set,UP)
        cjtoU = VGroup(cjtoU_set,cjtoU_label)
        cjtoV_set = Circle(radius = 1.5, fill_opacity = 0.6, stroke_opacity = 0).shift(1.8*LEFT).set_color(YELLOW)
        cjtoV_label = TextMobject("V").next_to(cjtoV_set,UP)
        cjtoV = VGroup(cjtoV_set,cjtoV_label)
        inter = SVGMobject("Topologia_SVGs/inter.svg", stroke_opacity = 0, fill_opacity = 0.8).shift(3*LEFT).scale(0.93) #A ojo para darle al tamaño
        inter_label = TexMobject(r" U \cap V").next_to(inter, 2*UP)
        intergroup = VGroup(inter,inter_label)
        abiertos_labels = VGroup(cjtoU_label,cjtoV_label)
        union_label = TexMobject(r" U \cup V").next_to(inter, 2.5*UP)
        
        
        #Primera propiedad
        prop_1 = TexMobject(r"1)\ A \subset U \cup V").shift(1*UP+1.8*RIGHT)

        #Segunda propiedad
        prop_2 = TexMobject(r"2)\ A \cap U \neq \varnothing\ \text{y}\ A \cap V \neq \varnothing").shift(3.2*RIGHT)

        #Tercera propiedad
        
        prop_3 = TexMobject(r"3)\ A \cap U \cap V = \varnothing").shift(1*DOWN+2.2*RIGHT)
        caracts = VGroup(prop_1,prop_2,prop_3)

        #Comenzamos con conexos
        conex_a = TextMobject("Un conjunto", " conexo", " es aquel que \\textbf{no} satisface")
        conex_a[1].set_color(BLUE)
        conex_b = TextMobject("al menos una de las tres propiedades anteriores.").next_to(conex_a,DOWN)
        conex = VGroup(conex_a, conex_b)
        ejs = TextMobject("Veamos algunos ejemplos:")
        
        satisface = TextMobject("Satisface").move_to(abiertos)
        no_satisface1 = TextMobject("\\textbf{No} satisface la primera propiedad, pues").shift(1*DOWN+3.2*RIGHT).scale(0.75)
        no_satisface2 = TextMobject("\\textbf{No} satisface la segunda propiedad, pues").shift(1*DOWN+3.2*RIGHT).scale(0.75)
        no_satisface3 = TextMobject("\\textbf{No} satisface la tercera propiedad, pues").shift(1*DOWN+3.2*RIGHT).scale(0.75)

        esconexo = TextMobject("Este conjunto es", " conexo").to_edge(DOWN)
        esconexo[1].set_color(BLUE)
        #Conexo1
        conexo1_svg = SVGMobject("Topologia_SVGs/conexo1.svg", stroke_opacity = 0, fill_opacity = 1, fill_color = BLUE).shift(3*LEFT).scale(0.5)
        conexo1_label = TextMobject("B").next_to(conexo1_svg,4*DOWN)
        conexo1 = VGroup(conexo1_svg,conexo1_label)

        conexo1_p1 = TexMobject(r" B \subset U \cup V").shift(1*UP+1.8*RIGHT)
        conexo1_p2 = TexMobject(r" B \cap U \neq \varnothing\ \text{y}\ B \cap V \neq \varnothing").shift(3.2*RIGHT)
        conexo1_p3 = TexMobject(r" B \cap U \cap V \neq \varnothing").next_to(no_satisface3,DOWN)
        
        textc1 = VGroup(satisface, conexo1_p1, conexo1_p2, conexo1_p3, no_satisface3)
        #Conexo2
        conexo2_svg = SVGMobject("Topologia_SVGs/conexo2.svg", stroke_opacity = 0, fill_opacity = 1, fill_color = BLUE).shift(4*LEFT).scale(0.5)
        conexo2_label = TextMobject("C").next_to(conexo2_svg,5*DOWN)
        conexo2 = VGroup(conexo2_svg,conexo2_label)
        conexo2_p1 = TexMobject(r" C \subset U \cup V").shift(1*UP+1.8*RIGHT)
        conexo2_p3 = TexMobject(r" C \cap U \cap V = \varnothing").shift(2.2*RIGHT)
        conexo2_p2 = TexMobject(r"\ C \cap V = \varnothing").next_to(no_satisface3,DOWN)
        textc2 = VGroup(satisface, conexo2_p1, conexo2_p2, conexo2_p3, no_satisface2)

        #Conexo3
        conexo3_svg = SVGMobject("Topologia_SVGs/conexo3.svg", stroke_opacity = 0, fill_opacity = 1, fill_color = BLUE).shift(3.05*LEFT+0.5*UP).scale(1.5)
        conexo3_label = TextMobject("D").next_to(conexo3_svg,3*UP)
        conexo3 = VGroup(conexo3_svg,conexo3_label)
        #Etiquetas de unión e interseccion para mostrar abajo
        inter_dlabel = TexMobject(r" U \cap V").next_to(inter, 2*DOWN)
        union_dlabel = TexMobject(r" U \cup V").next_to(inter, 2.5*DOWN)
        conexo3_p2 = TexMobject(r" D \cap U \neq \varnothing\ \text{y}\ D \cap V \neq \varnothing").shift(1*UP+3*RIGHT)
        conexo3_p3 = TexMobject(r" D \cap U \cap V = \varnothing").shift(2.2*RIGHT)
        conexo3_p1 = TexMobject(r" D \not\subset U \cup V").next_to(no_satisface3,DOWN)     
        textc3 = VGroup(satisface, conexo3_p1, conexo3_p2, conexo3_p3, no_satisface1)

        #Comentario final
        cfinal_a = TextMobject("¡Un conjunto formado por una sola pieza, (es decir", " conexo", ")")
        cfinal_a[1].set_color(BLUE)
        cfinal_b = TextMobject("nunca podrá satisfacer las tres propiedades!").next_to(cfinal_a,DOWN)
        cfinal = VGroup(cfinal_a,cfinal_b)

        #Secuencia de la animación
        self.play(Write(titulo))
        self.play(FadeOut(titulo))
        self.play(Write(intuitivo))
        self.wait(2)
        self.play(FadeOut(intuitivo))
        self.play(Write(tdisconexo))
        self.wait(2)
        self.play(FadeOut(tdisconexo))
        # Propiedades de un conjunto disconexo
        self.play(Write(el_disconexo))
        self.play(DrawBorderThenFill(disconexo),Write(disconexo_label))
        self.wait()
        self.play(Write(abiertos))
        self.bring_to_back(cjtoU)
        self.play(Write(cjtoU))
        self.bring_to_back(cjtoV)
        self.play(Write(cjtoV))
        self.play(Write(prop_1), abiertos_labels.set_opacity, 0)
        self.play(cjtoU_set.set_color, YELLOW, cjtoU_set.set_opacity, 1, cjtoV_set.set_opacity, 1, Write(union_label))
        self.wait(1.5)
        self.play(Write(prop_2))
        self.play(abiertos_labels.set_opacity, 1, FadeOut(union_label))
        self.play(cjtoU_set.set_color, ORANGE, cjtoU_set.set_opacity, 0.6, cjtoV_set.set_opacity, 0)
        self.wait(1.5)
        self.play(cjtoU_set.set_opacity, 0, cjtoV_set.set_opacity, 0.6)
        self.wait(1.5)
        self.play(cjtoU_set.set_opacity, 0.6, cjtoV_set.set_opacity, 0.6)
        self.wait()
        self.play(Write(prop_3))
        self.play(cjtoU_set.set_opacity, 0, cjtoV_set.set_opacity, 0.0, disconexo_label.shift, 2*LEFT, 
        abiertos_labels.set_opacity, 0)
        self.play(Write(inter_label))
        self.play(ShowCreation(inter))
        self.wait(1.5)
        self.play(FadeOut(inter))
        self.play(cjtoU_set.set_opacity, 0.6, cjtoV_set.set_opacity, 0.6, disconexo_label.shift, 2*RIGHT, 
        FadeOut(inter_label))
        self.wait()
        self.play(FadeOut(cjtoU_set),FadeOut(cjtoV_set),FadeOut(gdisconexo),FadeOut(caracts), 
        FadeOut(el_disconexo), FadeOut(abiertos))
        self.play(Write(conex))
        self.wait()
        self.play(FadeOut(conex))
        self.play(Write(ejs))
        self.wait()
        self.play(FadeOut(ejs))
        #ANIMACIÓN:PROPIEDADES CONEXO 1
        self.play(DrawBorderThenFill(conexo1))
        self.wait()
        self.play(Write(satisface))
        self.bring_to_back(cjtoU)
        self.bring_to_back(cjtoV)
        self.play(Write(cjtoU), Write(cjtoV), abiertos_labels.set_opacity, 1)
        self.wait()
        self.play(Write(conexo1_p1), abiertos_labels.set_opacity, 0)
        self.play(cjtoU_set.set_color, YELLOW, cjtoU_set.set_opacity, 1, cjtoV_set.set_opacity, 1, Write(union_label))
        self.wait(1.5)
        self.play(Write(conexo1_p2))
        self.play(abiertos_labels.set_opacity, 1, FadeOut(union_label))
        self.play(cjtoU_set.set_color, ORANGE, cjtoU_set.set_opacity, 0.6, cjtoV_set.set_opacity, 0)
        self.wait(1.5)
        self.play(cjtoU_set.set_opacity, 0, cjtoV_set.set_opacity, 0.6)
        self.wait(1.5)
        self.play(cjtoU_set.set_opacity, 0.6, cjtoV_set.set_opacity, 0.6)
        self.wait()
        self.play(Write(no_satisface3))
        self.play(Write(conexo1_p3))
        self.play(cjtoU_set.set_opacity, 0, cjtoV_set.set_opacity, 0.0, abiertos_labels.set_opacity, 0)
        self.play(Write(inter_label))
        self.play(ShowCreation(inter))
        self.wait()
        self.play(Write(esconexo))
        self.wait(1)
        self.play(FadeOut(textc1),FadeOut(intergroup), FadeOut(conexo1),FadeOut(esconexo))
        #ANIMACIÓN:PROPIEDADES CONEXO 2
        self.play(DrawBorderThenFill(conexo2))
        self.wait()
        self.play(Write(satisface))
        self.bring_to_back(cjtoU)
        self.play(cjtoU_set.set_color, ORANGE, cjtoU_set.set_opacity, 0.6, cjtoV_set.set_opacity, 0.6, abiertos_labels.set_opacity, 1)
        self.play(Write(conexo2_p1), abiertos_labels.set_opacity, 0)
        self.play(cjtoU_set.set_color, YELLOW, cjtoU_set.set_opacity, 1, cjtoV_set.set_opacity, 1, Write(union_label))
        self.wait(1.5)
        self.play(Write(conexo2_p3))
        self.play(FadeOut(union_label))
        self.play(cjtoU_set.set_color, ORANGE, cjtoU.set_opacity, 0.0, cjtoV.set_opacity, 0.0)
        self.play(Write(inter_label))
        self.play(ShowCreation(inter))
        self.wait(1.5)
        self.play(FadeOut(inter), FadeOut(inter_label))
        self.wait()
        self.play(Write(no_satisface2))
        self.play(Write(conexo2_p2))
        self.play(Write(cjtoV_label))
        self.play(cjtoV.set_opacity, 0.6)
        self.wait()
        self.play(Write(esconexo))
        self.wait(1)
        self.play(FadeOut(conexo2), FadeOut(textc2), FadeOut(esconexo), cjtoV.set_opacity, 0)
        #ANIMACIÓN:PROPIEDADES CONEXO 3
        self.play(Write(conexo3))
        self.wait()
        self.play(cjtoU_set.set_color, ORANGE, cjtoU_set.set_opacity, 0.6,
        cjtoV_set.set_color, YELLOW, cjtoV_set.set_opacity, 0.6, cjtoU_label.set_opacity, 1, cjtoV_label.set_opacity, 1)
        self.play(Write(satisface))
        self.play(Write(conexo3_p2))
        self.play(cjtoU.set_opacity, 0.6, cjtoV.set_opacity, 0)
        self.wait(1.5)
        self.play(cjtoU.set_opacity, 0, cjtoV.set_opacity, 0.6)
        self.wait(1.5)
        self.play(cjtoU_set.set_opacity, 0.6, cjtoV_set.set_opacity, 0.6, abiertos_labels.set_opacity , 1)
        self.wait()
        self.play(Write(conexo3_p3))
        self.play(cjtoU.set_opacity, 0, cjtoV.set_opacity, 0.0)
        self.play(Write(inter_dlabel))
        self.play(ShowCreation(inter))
        self.wait()
        self.play(Write(no_satisface1), FadeOut(inter), FadeOut(inter_dlabel))
        self.bring_to_back(cjtoU)
        self.bring_to_back(cjtoV)
        self.play(cjtoU_set.set_opacity, 0.6, cjtoV_set.set_opacity, 0.6, abiertos_labels.set_opacity , 1)
        self.play(Write(conexo3_p1))
        self.play(cjtoU_set.set_color, YELLOW, cjtoU_set.set_opacity, 1, cjtoV_set.set_opacity, 1,
        abiertos_labels.set_opacity, 0, Write(union_dlabel))
        self.wait(1.5)
        self.play(Write(esconexo))
        self.wait()
        self.play(FadeOut(textc3), FadeOut(conexo3), FadeOut(esconexo), FadeOut(cjtoU_set), FadeOut(cjtoV_set), FadeOut(union_dlabel))
        #Comentario fnal
        self.play(Write(cfinal))
        self.wait(2)
        self.play(FadeOut(cfinal))

#############################
#### CONJUNTOS CONVEXOS #####
#############################

class ConjuntosConvexos(Scene):
    def construct(self):
        #Título y texto
        titulo = TextMobject("Conjuntos convexos")
        pregunta = TextMobject("¿Cual es la diferencia entre estos dos conjuntos?").to_edge(UP)

        #Conjunto convexo(izq)
        lao_svg = SVGMobject('Topologia_SVGs/convexo.svg').set_height(FRAME_HEIGHT*0.4).shift(3*LEFT)
        lao_svg.set_style(fill_opacity=0.7,stroke_width=0,stroke_opacity=1,fill_color=BLUE)
        lao_label = TextMobject("A").next_to(lao_svg,DOWN)
        lao = VGroup(lao_svg,lao_label)
        #Conjunto no-convexo(der)
        lau_svg = SVGMobject('Topologia_SVGs/no_convexo.svg').set_height(FRAME_HEIGHT*0.4).shift(3*RIGHT)
        lau_svg.set_style(fill_opacity=0.5,stroke_width=0,stroke_opacity=1,fill_color=YELLOW)
        lau_label = TextMobject("B").next_to(lau_svg,DOWN)
        lau = VGroup(lau_svg,lau_label)
        #"En un lenguaje casual"
        casual_1 = TextMobject("En un lenguaje casual, podríamos decir que el").to_edge(UP)
        casual_2 = TextMobject("conjunto B tiene una hendidura. ").next_to(casual_1, DOWN)
        casual = VGroup(casual_1,casual_2)
        formal = TextMobject("Formalicemos lo anterior.").to_edge(DOWN).scale(1.1)
        
        # Definición segmento de recta
        equis_dot = Dot(point = (-3,1,0))
        equis_label = TexMobject(r"\vec{x}").next_to(equis_dot,UP+LEFT)
        equis = VGroup(equis_dot, equis_label)
        ye_dot = Dot(point = (3,-1,0))
        ye_label = TexMobject(r"\vec{y}").next_to(ye_dot,DOWN+RIGHT)
        ye = VGroup(ye_dot,ye_label)
        segmento_a= TextMobject("Dados dos puntos en $\mathbb{R}^n$ definimos el segmento que los une como:").to_edge(UP).scale(0.9)
        segmento = Line(start = (-3,1,0), end = (3,-1,0))
        segmento_b = TexMobject(r"[\vec{x},\vec{y}]=\{ (1-t)\vec{x}+t\vec{y}\in \mathbb{R}^n | t\in [0,1]\}").to_edge(DOWN)

        #Centrado conjunto convexo
        lao_svg_1 = SVGMobject('Topologia_SVGs/convexo.svg').set_height(FRAME_HEIGHT*0.4)
        lao_svg_1.set_style(fill_opacity=0.7,stroke_width=0,stroke_opacity=1,fill_color=BLUE)
        Acomment = TextMobject("Para cualesquiera dos puntos $\\vec{x},\\vec{y} \\in$ A,  tenemos que $[\\vec{x},\\vec{y}]\\subset$ A").to_edge(UP).scale(0.9)
        ## Pares de puntos para A 
        par_A1 = VGroup(Dot(point = (1,1,0)),Dot(point = (-1,-1,0)), Line(start = (1,1,0),end = (-1,-1,0)))
        par_A2 = VGroup(Dot(point = (0,1,0)),Dot(point = (0,-1,0)), Line(start = (0,1,0),end = (0,-1,0)))
        par_A3 = VGroup(Dot(point = (-0.7,1.1,0)),Dot(point = (0.5,-1.1,0)), Line(start = (-0.7,1.1,0),end = (0.5,-1.1,0)))
        convexo = TextMobject("A esto se le conoce como un \"conjunto convexo\".").to_edge(DOWN).scale(0.9)

        # Centrado conjunto no convexo
        lau_svg_1 = SVGMobject('Topologia_SVGs/no_convexo.svg').set_height(FRAME_HEIGHT*0.4)
        lau_svg_1.set_style(fill_opacity=0.5,stroke_width=0,stroke_opacity=1,fill_color=YELLOW)
        Bcomment_a = TextMobject("Esto no sucede para el conjunto B, pues").to_edge(UP)
        Bcomment_b = TextMobject("extisten $\\vec{x},\\vec{y}\\subset$ B tales que $[\\vec{x},\\vec{y}]\\not\\subseteq$ B").next_to(Bcomment_a,DOWN)
        Bcomment = VGroup(Bcomment_a,Bcomment_b).scale(0.9)
        ##Pares de puntos para B
        par_B1 = VGroup(Dot(point = (-0.5,1,0)), Dot(point =(-0.5,-1,0)), Line(start =(-0.5,1,0),end =(-0.5,-1,0)))
        par_B2 = VGroup(Dot(point = (-0.2,-1,0)),Dot(point = (0.7,-1,0)), Line(start =(-0.2,-1,0),end =(0.7,-1,0)))
        par_B3 = VGroup(Dot(point = (-0.8,1,0)), Dot(point = (0.8,1,0)), Line(start =(-0.8,1,0),end =(0.8,1,0))).set_color(RED)
        no_convexo = TextMobject("Este conjunto es no convexo.").to_edge(DOWN).scale(0.9)

        entonces = TextMobject("Entonces, de manera formal:").to_edge(UP)
        lao_conv = TextMobject("Convexo").next_to(lao_label,2*DOWN)
        lau_nconv = TextMobject("No convexo").next_to(lau_label, 2*DOWN)

        # Secuencia de la animación
        self.play(Write(titulo))
        self.wait()
        self.play(FadeOut(titulo))
        self.play(Write(pregunta))
        self.play(Write(lao),Write(lau))
        self.wait()
        self.play(FadeOut(pregunta))
        self.play(Write(casual))
        self.wait()
        self.play(Write(formal))
        self.wait()
        self.play(FadeOut(casual),FadeOut(formal),FadeOut(lao),FadeOut(lau))
        self.play(Write(equis),Write(ye))
        self.play(Write(segmento_a))
        self.play(Write(segmento),Write(segmento_b))
        self.wait(2)
        self.play(FadeOut(equis),FadeOut(ye),FadeOut(segmento),FadeOut(segmento_a),FadeOut(segmento_b))
        self.play(Write(lao_svg_1))
        self.play(Write(Acomment))
        self.bring_to_back(lao_svg_1)
        self.play(ShowCreation(par_A1))
        self.wait(1.2)
        self.play(ReplacementTransform(par_A1,par_A2))
        self.wait(1.2)
        self.play(ReplacementTransform(par_A2,par_A3))
        self.wait(1.2)
        self.play(Write(convexo))
        self.wait()
        self.play(FadeOut(Acomment),FadeOut(convexo),FadeOut(lao_svg_1),FadeOut(par_A3)) 
        self.play(Write(lau_svg_1))
        self.play(Write(Bcomment))
        self.bring_to_back(lau_svg_1)
        self.wait()
        self.play(ShowCreation(par_B1))
        self.wait(1.2)
        self.play(ReplacementTransform(par_B1,par_B2))
        self.wait(1.2)
        self.play(ReplacementTransform(par_B2,par_B3))
        self.play(par_B3.scale, 1.4)
        self.play(par_B3.scale, 1/1.4)
        self.wait()
        self.play(Write(no_convexo))
        self.wait()
        self.play(FadeOut(Bcomment),FadeOut(no_convexo),FadeOut(lau_svg_1),FadeOut(par_B3))
        self.play(Write(entonces))
        self.play(Write(lao),Write(lau))
        self.play(Write(lao_conv))
        self.play(Write(lau_nconv)) 
        self.wait(2)
        self.play(FadeOut(entonces),FadeOut(lao),FadeOut(lau),FadeOut(lao_conv),FadeOut(lau_nconv))