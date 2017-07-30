class ola():
    def draw_screen(self, display, centerX, centerY, fix_r, posX, posY):
        with display.canvas:
            bar_weight = 0.15
            bar_relative_pos = 0.8
            Rectangle(pos=(centerX - abs(centerX * bar_relative_pos), centerY),
                      size=(centerX * bar_weight, (float(power_LEFT / 100)) * fix_r))
            Rectangle(pos=(centerX + abs(centerX * (bar_relative_pos - bar_weight)), centerY),
                      size=(centerX * bar_weight, (float(power_RIGHT / 100)) * fix_r))

            # positions
            xleft = centerX - abs(centerX * bar_relative_pos)
            xright = centerX + abs(centerX * (bar_relative_pos - bar_weight))
            b_width = centerX * bar_weight
            b_height = fix_r
            Line(points=[xleft, centerY - b_height, xleft, centerY + b_height, xleft + b_width, centerY + b_height,
                         xleft + b_width, centerY - b_height], width=0.5, close=True, joint='round')
            Line(points=[xright, centerY - b_height, xright, centerY + b_height, xright + b_width, centerY + b_height,
                         xright + b_width, centerY - b_height], width=0.5, close=True, joint='round')

            #### END OF POWER MOTORS MECHANICHS
            z = []
            widget3 = Label(text='[b]' + 'Power ' + str(round(power_LEFT, 1)) + ' % ' + '[/b]',
                            pos=(xleft * 1.1, centerY + fix_r * 1.1),
                            size=[1, 1],
                            font_size='16sp', markup=True)

            widget2 = Label(text='[b]' + 'Power ' + str(round(power_RIGHT, 1)) + ' % ' + '[/b]',
                            pos=(xright, centerY + fix_r * 1.1),
                            size=[1, 1],
                            font_size='16sp', markup=True)

            widget4 = Label(text='[b]' + 'Forward ' + '[/b]',
                            pos=(centerX, centerY + fix_r * 1.1),
                            size=[1, 1],
                            font_size='20sp', markup=True)

            widget5 = Label(text='[b]' + 'Backward ' + '[/b]',
                            pos=(centerX, centerY - fix_r * 1.1),
                            size=[1, 1],
                            font_size='20sp', markup=True)

            z.append([widget2, widget3, widget4, widget5])

            self.z = z

            Color(0, 0, 0, 0)
            Rectangle(pos=(0, 0), size=display.size)

            Color(1, 1, 1, 1)
            Line(points=[centerX, centerY, posX, posY], width=1.3, close=True, joint='round')

            Color(1, 1, 1, 1)
            Line(circle=(centerX, centerY, fix_r * 1.01, 0, 360), width=1.3)
            Line(circle=(centerX, centerY, fix_r * 0.53, 0, 360), width=0.9)

            # Line(points=[centerX, centerY, centerX, centerY + fix_r], width=0.5, close=True, joint='round')
            Line(points=[centerX, centerY, centerX + fix_r, centerY], width=0.5, close=True, joint='round')
            Line(points=[centerX, centerY, centerX - fix_r, centerY], width=0.5, close=True, joint='round')

            ##### LABELS IN THE CIRCLES PUSHMATRIX a POPMATRIX zapricini ze prikaz rotace se neuplatni v celem canvas ale jen mezi temito dvema prikazy
            z = []
            PushMatrix()
            r = Rotate()
            r.angle = 0

            widget = Label(text='[b]' + 'Puls' + '[/b]', pos=[centerX, centerY - fix_r * 0.7], size=[1, 1],
                           font_size='20sp', markup=True, )
            z.append(widget)
            PopMatrix()