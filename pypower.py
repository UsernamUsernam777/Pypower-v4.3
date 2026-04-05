import _datetime
import ast as _ast
import customtkinter as _ctk
import pyperclip as _pyperclip
import time as _time
import webbrowser as _webbrowser
import os as _os
import subprocess as _ubprocess
class Time:
    @staticmethod
    def minus_clock(time_str1, time_str2):
        t1 = Time.reverse_many_hms(time_str1)
        t2 = Time.reverse_many_hms(time_str2)
        return Time.how_many_hms_in_s(abs(t1-t2))
    """convert time to type_output"""
    @staticmethod
    def how_many_hms_in_s(sec):
        """how many hours, minutes and seconds in seconds"""
        hours = int(sec // 3600)
        minutes = int((sec % 3600) // 60)
        seconds = int((sec % 3600) % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    @staticmethod
    def reverse_many_hms(time_str):
        result = Time.convert_to_iterable_and_int(time_str)
        return (result[0]*3600) + (result[1]*60) + result[2]
    @staticmethod
    def in_bg(duration, action=None):
        """Run action in a background thread after duration seconds."""
        t = _ctk.CTk()
        t.after(duration*1000, action)
class Apps:
    @staticmethod
    def create_app(path, icon=None, move_to_folder=None, name=None):
        """Build a standalone .exe from a .py file using PyInstaller, then clean up build files."""
        def mainloop():
            from shutil import rmtree
            if not _os.path.exists(path):
                print('Error!')
            else:
                pj = _os.path.dirname(path)
                n_py = _os.path.basename(path)
                n_exe = _os.path.basename(path).replace('.py', '.exe')
                n_spec = _os.path.basename(path).replace('.py', '.spec')
                pro = ['pyinstaller', '--onefile', '--windowed', n_py]
                _os.chdir(pj)
                if icon:
                    pro.append(f'--icon={icon}')
                if name:
                    pro.append(f'--name={name}')
                p = _subprocess.Popen(pro, creationflags=_subprocess.CREATE_NO_WINDOW)
                p.wait()
                if _os.path.exists(_os.path.join('dist', n_exe)):
                    _os.replace(_os.path.join('dist', n_exe), _os.path.join(pj, n_exe))
                if _os.path.exists(_os.path.join(pj, n_exe)):
                    rmtree('dist', ignore_errors=True)
                    rmtree('build', ignore_errors=True)
                    _os.remove(n_spec)
                if _os.path.exists(path.replace('.py', '.exe')):
                    if move_to_folder:
                        new = _os.path.join(move_to_folder, n_exe)
                        _os.replace(path.replace('.py', '.exe'), new)
                    else:
                        new = path.replace('.py', '.exe')
                    print(f"App Created Successed in {new}")
        Other.in_bg(1, mainloop)
class Files:
    @staticmethod
    def in_bg(duration, action=None):
        a = globals()
        found = False
        for i in alls:
            if isinstance(a[i], _ctk.CTk):
                i.after(duration, action)
                found = True
                break
        if not found:
            a = _ctk.CTk()
            a.after(duration, action)
    @staticmethod
    def read_write_txt_file(file_txt, do='read', text=None, create_if_no=False):
        if create_if_no:
            Files.make_if_not_exists(file_txt, 'txt')
        if do == 'read':
            with open(file_txt, 'r', encoding='utf-8') as f:
                return f.read().strip()
        else:
            if _os.path.exists(file_txt):
                with open(file_txt, 'w', encoding='utf-8') as f:
                    f.write(text or '')
    @staticmethod
    def make_if_not_exists(path, type=''):
        """Create a folder (type='') or empty file at path if it doesn't exist."""
        if not _os.path.exists(path):
            if type == '':
                _os.mkdir(path)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    pass
    @staticmethod
    def append_to_pypower(path, class_name, code):
        """Append a labeled code block to pypower.py."""
        Files.append_to_file(path, f'\n#{class_name}\n'+code)
    @staticmethod
    def append_to_file(path, text, side='bottom'):
        """Append text to a file removing double blank lines."""
        old_text = Files.read_write_txt_file(path)
        with open(path, 'w', encoding='utf-8') as b:
            if side == 'top':
                new_text = text + '\n' + old_text
            else:
                new_text = old_text + '\n' + text
            b.write(new_text.replace('\n\n', '\n'))
class GUI:
    class CustomTk:
        class Manager:
            def clear_manager(dic):
                no = ['width', 'height', 'in', 'relwidth', 'relheight']
                for n in no:
                    if n in dic:
                        dic.pop(n)
                for i in dic:
                    if Math.int_or_float(dic[i]):
                        dic[i] = float(dic[i])
                return dic
            def manager_with_data(obj, manager, dic):
                dic = GUI.CustomTk.Manager.clear_manager(dic)
                getattr(obj, manager)(**dic)
            def places_from_file(file, master):
                Files.make_if_not_exists(file, 'txt')
                dicts = String(Files.read_write_txt_file(file)).between('{', '}')
                if dicts:
                    for i in range(len(dicts)):
                        dicts[i] = _ast.literal_eval(dicts[i])
                    for i, e in zip(sorted(GUI.CustomTk.all_objects(master), key=str), dicts):
                        GUI.CustomTk.Manager.manager_with_data(i, i.winfo_manager(), e)
            def places_to_file(file, master):
                cl = GUI.CustomTk.Manager.clear_manager
                s = ''
                for i in sorted(GUI.CustomTk.all_objects(master), key=str):
                    t = i.winfo_manager()
                    t = cl(getattr(i, f'{t}_info')())
                    s += str(t) + '\n'
                Files.read_write_txt_file(file, 'write', s.strip('\n'), True)
            def manager_same(obj1, obj2):
                cl = GUI.CustomTk.Manager.clear_manager
                t = obj1.winfo_manager()
                if t:
                    n = cl(getattr(obj1, f'{t}_info')())
                    getattr(obj2, f'{t}')(**n)
        def copy_style(master, all_objects=True):
            if all_objects:
                wids = GUI.CustomTk.has_text_iterable(GUI.CustomTk.all_objects(master))
            else:
                wids = GUI.CustomTk.has_text_iterable(master.winfo_children())
            def alls():
                in_mode = True
                def c(obj1, obj2):
                    atts = {}
                    for i in ['fg_color', 'bg_color', 'font', 'text_color']:
                        atts[i] = obj1.cget(i)
                    obj2.configure(**atts)
                new = []
                def fi(e):
                    nonlocal in_mode
                    if in_mode:
                        new.append(e.widget.master)
                        if len(new) == 2:
                            c(new[0], new[1])
                            new.clear()
                            in_mode = False
                for i in wids:
                    i.bind('<Button-1>', fi)
            btn = _ctk.CTkButton(master, text='copy style', command=alls)
            return btn
        def dont_enter(entry, iterable):
            if entry.cget('textvariable'):
                check = entry.cget('textvariable')
            else:
                check = _ctk.StringVar()
                entry.configure(textvariable=check)
            def c(*args):
                if check.get()[-1] in iterable:
                    entry.delete(entry.index('insert') - 1)
            check.trace_add('write', c)
        def len_entry(entry, text_with_num='', with_spaces=True):
            if entry.cget('textvariable'):
                check = entry.cget('textvariable')
            else:
                check = _ctk.StringVar()
                entry.configure(textvariable=check)
            label = _ctk.CTkLabel(entry.master, text=f'{text_with_num}0')
            def c(*args):
                lenth_text = len(check.get()) if with_spaces else len(check.get().replace(' ', ''))
                lenth_all = f"{text_with_num}{lenth_text}"
                label.configure(text=lenth_all)
            check.trace_add('write', c)
            return label
        def label_widget(obj, message, side='above', value=0, text_color='black', font=('arial', 10), fg_color=None):
            l = _ctk.CTkLabel(obj.master, text=message, text_color=text_color, font=font, fg_color=fg_color)
            def m():
                l.lift()
                if side == 'above':
                    l.place(x=obj.winfo_x(), y=obj.winfo_y()-obj.winfo_height())
                else:
                    l.place(x=obj.winfo_x(), y=obj.winfo_y()+obj.winfo_height())
            obj.master.after(200, m)
        def entry_label(obj):
            is_label = isinstance(obj, _ctk.CTkLabel)
            event = "<Shift-Double-Button-1>" if is_label else "<Return>"
            atts = ['fg_color', 'text_color', 'font']
            if obj.cget('fg_color') == 'transparent':
                atts.remove('fg_color')
            attributes = {i: obj.cget(i) for i in atts}
            def convert(e):
                if is_label:
                    a = _ctk.CTkEntry(obj.master)
                else:
                    a = _ctk.CTkLabel(obj.master)
                a.configure(**attributes)
                a.configure(corner_radius=obj.cget('corner_radius')+1)
                def m():
                    x = obj.winfo_x()
                    y = obj.winfo_y()
                    if is_label:
                        a.insert(0, obj.cget('text'))
                    else:
                        a.configure(text=obj.get())
                    a.place(x=x, y=y)
                    obj.destroy()
                    GUI.CustomTk.entry_label(a)
                obj.after(200, m)
            obj.bind(event, convert)
        def options(widget, names, commands, font=('arial', 10), text_color='white'):
            a = _ctk.CTkFrame(widget.master)
            from itertools import zip_longest
            for i, e in zip_longest(names, commands):
                l = _ctk.CTkButton(a, text=i, text_color=text_color, font=font, width=len(i)+50, height=font[1])
                l.pack()
                l.configure(command=e)
            def show(e):
                def m():
                    a.lift()
                    a.place(x=widget.winfo_x()+1, y=widget.winfo_y()+widget.winfo_height())
                widget.after(200, m)
            widget.bind("<Button-3>", show)
            widget.master.bind("<Button-1>", lambda e:a.place_forget())
        def table(master, dic_data, font=('arial', 30), text_color='black', buttons=False, widgets_frame=False, autofit=False):
            a = _ctk.CTkScrollableFrame(master)
            widgets = []
            col_num = 0
            for k in dic_data:
                col = []
                if buttons:
                    col.append(_ctk.CTkButton(a, text=k, font=font, text_color=text_color))
                else:
                    col.append(_ctk.CTkLabel(a, text=k, font=font, text_color=text_color))
                for v in dic_data[k]:
                    if buttons:
                        col.append(_ctk.CTkButton(a, text=v, font=font, text_color=text_color))
                    else:
                        col.append(_ctk.CTkLabel(a, text=v, font=font, text_color=text_color))
                GUI.CustomTk.tidy_up(col, per_row=1, start_column=col_num)
                col_num += 1
                if autofit:
                    GUI.CustomTk.good_size(col)
                if widgets_frame:
                    widgets.extend(col)
            if widgets_frame:
                return {'widgets': widgets, 'frame': a}
            return a
        def duplicate_double_click(obj, move=False):
            def alls(e):
                new = GUI.CustomTk.clone_widget(obj)
                new.lift()
                if move:
                    GUI.CustomTk.move(new)
                obj.after(300, lambda:new.place(x=obj.winfo_x(), y=obj.winfo_y()+obj.winfo_height()))
                GUI.CustomTk.duplicate_double_click(new)
            obj.bind('<Double-Button-1>', alls)
        def clone_widget(widget, master=None):
            new = widget.__class__(master or widget.master)
            attr = widget.__dict__
            for i in attr:
                try:
                    if i[0] == '_':
                        new_config = {i[1:]: attr[i]}
                    else:
                        new_config = {i: attr[i]}
                    new.configure(**new_config)
                except:
                    pass
            new.configure(width=attr['_current_width'], height=attr['_current_height'])
            return new
        def add_texts_to_file(master, file, title):
            Files.make_if_not_exists(file, 'txt')
            new = str(GUI.CustomTk.has_text_iterable(GUI.CustomTk.all_objects(master), text_obj=True)['texts'])
            Files.append_to_file(file, title + String(new).replace_many(['[', ']', ', '], ['', '', '\n']))
        def has_text(obj, with_empty=False):
            try:
                obj.cget('text')
                if with_empty:
                    assert obj.cget('text').strip()
                return True
            except:
                return False
        def has_text_iterable(iterable, with_empty=False, text_obj=False):
            result = []
            for i in iterable:
                if GUI.CustomTk.has_text(i, with_empty):
                    result.append(i)
            if text_obj:
                return {'texts': [t.cget('text') for t in result], 'widgets': result}
            return result
        def show_hide_message(master, message, text_color='red', font=('arial', 30), x=None, y=None, show_after=0, hide_after=1, in_btn=False):    
            if in_btn:
                a = _ctk.CTkButton(master, text=message, font=font, text_color=text_color, hover=False, )
            else:
                a = _ctk.CTkLabel(master, text=message, font=font, text_color=text_color)
            def s():
                if x and y:
                    a.place(x=x, y=y)
                else:
                    a.pack()
                a.after(int(hide_after*1000), a.destroy)
            a.after(int(show_after*1000), s)
            return a
        def change_mode(master, light_icon='light', dark_icon='dark'):
            def c():
                icons = [dark_icon, light_icon]
                modes = ['Light', 'Dark']
                _ctk.set_appearance_mode(Iterable.opponents(modes, _ctk.get_appearance_mode()))
                button.configure(text=Iterable.opponents(icons, button.cget('text')))
            button = _ctk.CTkButton(master, text=dark_icon, command=c, font=('arial', 30))
            return button
        def limit_len(entry, limit):
            if entry.cget('textvariable'):
                check = entry.cget('textvariable')
            else:
                check = _ctk.StringVar()
                entry.configure(textvariable=check)
            def c(*args):
                if len(entry.get()) > limit:
                    entry.delete(entry.index('insert') - 1)
            check.trace_add('write', c)
        def sync_entry_with_label(entry, label):
            if entry.cget('textvariable'):
                var = entry.cget('textvariable')
            else:
                var = _ctk.StringVar()
            var.trace_add('write', lambda *args:label.configure(text=entry.get()))
            entry.configure(textvariable=var)
        def console(master, texts, per_row=3, entry_to_insert=None, font=('arial', 20), text_color='white', return_dic_frame_and_buttons=False):
            result = _ctk.CTkFrame(master)
            def create_button(text):
                if entry_to_insert:
                    return _ctk.CTkButton(result, text=text, font=font, text_color=text_color, command=lambda: entry_to_insert.insert('end', text))
                return _ctk.CTkButton(result, text=text, font=font, text_color=text_color)
            buttons = [create_button(str(c)) for c in texts]
            GUI.CustomTk.tidy_up(buttons, per_row=per_row)
            if return_dic_frame_and_buttons:
                return {'frame': result, 'buttons': buttons}
            return result
        class Timer:
            def __init__(self, duration, obj, start_icon='start', stop_icon='stop', while_resume=None, when_finish=None):
                self.duration = duration
                self.resume = self.duration > 0
                self.obj = obj
                self.obj.configure(text=Time.how_many_hms_in_s(self.duration))
                self.button = _ctk.CTkButton(obj.master, text=start_icon, command=self.start)
                self.start_icon = start_icon
                self.stop_icon = stop_icon
                self.timers = 0
                self.while_resume = while_resume
                self.when_finish = when_finish
            def start(self):
                if self.resume:
                    self.button.configure(command=self.stop, text=self.stop_icon)
                    self.duration -= 1
                    self.obj.configure(text=Time.how_many_hms_in_s(self.duration))
                    if self.while_resume:
                        self.while_resume()
                    if self.duration == 0:
                        if self.when_finish:
                            self.button.configure(text=self.start_icon)
                            self.when_finish()
                    else:
                        self.obj.after(1000, self.start)
            def stop(self):
                self.button.configure(command=self.resume_timer, text=self.start_icon)
                self.resume = False
            def resume_timer(self):
                self.resume = self.duration > 0
                self.start()
        def show_hide_entry_btn(entry, show_ico="show", hide_ico='hide', hide_with="*"):
            entry.configure(show=hide_with)
            btn = _ctk.CTkButton(entry.master, text=show_ico, font=("arial", 20))
            def change():
                if entry.cget("show") == hide_with:
                    entry.configure(show='')
                    btn.configure(text=hide_ico)
                else:
                    entry.configure(show=hide_with)
                    btn.configure(text=show_ico)
            btn.configure(command=change)
            return btn
        def move(obj, action_when_move=None, lift_when_move=False):
            master = obj.master
            def m(e):
                x = obj.winfo_x()
                y = obj.winfo_y()
                obj.pack_forget()
                obj.grid_forget()
                obj.place(x=x, y=y)
                width = obj.winfo_width()
                height = obj.winfo_height()
                mouse_x = master.winfo_pointerx() - master.winfo_rootx() - width//2
                mouse_y = master.winfo_pointery() - master.winfo_rooty() - height//2
                obj.place(x=mouse_x, y=mouse_y)
                if lift_when_move:
                    obj.lift()
                if action_when_move:
                    action_when_move()
            obj.bind('<B1-Motion>', m)
        def good_size(widgets):
            """resize widgets with the biggest size (height, width)"""
            def m():
                width = [i.winfo_reqwidth() for i in widgets]
                height = [i.winfo_reqheight() for i in widgets]
                for i in widgets:
                    i.configure(width=max(width), height=max(height))
            widgets[0].after(100, m)
        def sort_colors(widgets, per_row_color, start_col=0, start_row=0, color_of='fg_color', orientation='vertical'):
            sc = start_col
            sr = start_row
            colors = set()
            for i in widgets:
                v = i.cget(color_of)
                if isinstance(v, list):
                    colors.add(v[0])
                else:
                    colors.add(v)
            wids = []
            for i in colors:
                new = []
                for o in widgets:
                    if o.cget(color_of) == i:
                        new.append(o)
                wids.append(new)
            for i in wids:
                GUI.CustomTk.tidy_up(i, per_row_color, start_row=sr, start_column=sc)
                if orientation == 'vertical':
                    sc += per_row_color
                else:
                    sr += (len(i) // per_row_color) + 1
        def tidy_up(widgets, per_row, start_row=0, start_column=0, padx=5, pady=5):
            master = widgets[0].master
            """
            Arrange widgets in a grid with a fixed number per row.
            """
            for i in range(start_row):
                master.grid_rowconfigure(i, minsize=widgets[0].winfo_reqheight())
            for i in range(start_column):
                master.grid_columnconfigure(i, minsize=widgets[0].winfo_reqwidth())
            columns = start_column
            rows = start_row
            allowed_num = 0
            multy = range(per_row, len(widgets)+1, per_row)
            for w in widgets:
                w.grid(column=columns, row=rows, padx=padx, pady=pady)
                allowed_num += 1
                columns += 1
                if allowed_num in multy:
                    rows += 1
                    columns = start_column
        def all_objects(master):
            """Return a flat list of all child widgets in master."""
            result = []
            for i in master.winfo_children():
                if isinstance(i, (_ctk.CTkFrame, _ctk.CTkScrollableFrame)):
                    result.extend(GUI.CustomTk.all_objects(i))
                else:
                    result.append(i)
            return result
        def edit_all_widgets_texts(iterable, font='arial', size=20, text_color='lightblue', bg='', with_empty=False):
            """Apply font, text color, and background to all child widgets in master."""
            def m():
                for i in GUI.CustomTk.has_text(iterable, with_empty=with_empty):
                    if bg:
                        i.configure(font=(font, size), text_color=text_color, fg_color=bg)    
                    else:
                        i.configure(font=(font, size), text_color=text_color, fg_color='transparent')
            iterable[0].master.after(len(iterable) // 1000, m)
        def info(widget, information, font='arial', size=20, bg='', hide_after=5):
            """Show a tooltip label below widget on hover, auto-hide after hide_after seconds."""
            if bg:
                inf = _ctk.CTkLabel(widget.master, text=information, font=(font, size), fg_color=bg)
            else:
                inf = _ctk.CTkLabel(widget.master, text=information, font=(font, size), fg_color='transparent')
            inf.lift()
            widget.bind('<Leave>', lambda e: inf.place_forget())
            def show(e):
                x = widget.winfo_x()
                y = widget.winfo_y()
                inf.after(500, lambda: inf.place(x=x, y=y+widget.winfo_height()))
                inf.after(int(hide_after*1000), inf.place_forget)
            widget.bind('<Enter>', show)
        def mouse_wheel_num(entry, end, step=1):
            """Scroll through numbers inside an entry with the mouse wheel."""
            def f(e):
                if Math.int_or_float(entry.get()):
                    a = float(entry.get())
                    entry.delete(0, 'end')
                    if e.delta >= 1:
                        new_num = type(step)(a + step)
                    else:
                        new_num = type(step)(a - step)
                    if a == end:
                        new_num = 0
                    entry.insert(0, round(new_num, 2))
            entry.bind("<MouseWheel>", f)
    class Turtle:
        def moving(obj, keys, value=20, when_moving=None):
            """insert keys with this order: [up, down, left, right]"""
            def up():
                obj.setheading(90)
                obj.forward(value)
                if when_moving:
                    when_moving()
            def down():
                obj.setheading(270)
                obj.forward(value)
                if when_moving():
                    when_moving()
            def left():
                obj.setheading(180)
                obj.forward(value)
                if when_moving:
                    when_moving()
            def right():
                obj.setheading(0)
                obj.forward(value)
                if when_moving:
                    when_moving()
            for i, e in zip(keys, [up, down, left, right]):
                obj.screen.onkeypress(e, i)
        def in_circle(turtle_obj, shape_as_func, how_many=10):
            """draw shape_as_func in circle"""
            for i in range(how_many):
                shape_as_func()
                turtle_obj.left(360/how_many)
        def rock_bottom(window, obj, before_end=20, on_xy=False):
            x = window.window_width() // 2 - before_end
            y = window.window_height() // 2 - before_end
            if on_xy:
                if abs(obj.xcor()) >= abs(x):
                    return 'x'
                elif abs(obj.ycor()) >= abs(y):
                    return 'y'
                else:
                    return ''
            return abs(obj.xcor()) >= abs(x) or abs(obj.ycor()) >= abs(y)
class String:
    def __init__(self, text):
        self.text = text
    def super_join(self, sep, after_how_many_letters):
        """Insert sep every after_how_many_letters characters in the string."""
        value = 0
        new = ''
        ran = range(after_how_many_letters, len(self.text)-1, after_how_many_letters)
        for i in self.text:
            new += i
            value += 1
            if value in ran:
                new += sep
        return new
    def reverse(self, sep):
        """Reverse the order of parts split by sep. ex: 'a-b-c' -> 'c-b-a'"""
        return f'{sep}'.join(self.text.split(sep)[::-1])
    def replace_objects_with_one(self, iterable, new_obj=''):
        """Replace every character found in iterable with new_obj."""
        result = ''
        for i in self.text:
            if i not in iterable:
                result += i
            else:
                result += new_obj
        return result
    def replace_many(self, old_iterable, new_iterable):
        """Replace each character in old_iterable with the matching one in new_iterable."""
        for i, e in zip(old_iterable, new_iterable):
            self.text = self.text.replace(i, e)
        return self.text
    def between(self, c1, c2, first=True, last=True):
        """return string between two points"""
        result = []
        index = [Iterable.indexes(self.text, c1), Iterable.indexes(self.text, c2)]
        for i, e in zip(index[0], index[1]):
            if not first:
                i += 1
            if last:
                e += 1
            result.append(self.text[i:e])
        return result
    def line_if_in(self, string):
        result = []
        for i in self.split('\n'):
            if string in i:
                result.append(i)
        return result
class Iterable:
    @staticmethod
    def opponents(iterable, obj):
        """takes iterable for 2 elements and if the obj == anyone, the function returns the other one"""
        if obj == iterable[0]:
            return iterable[1]
        elif obj == iterable[1]:
            return iterable[0]
        return obj
    @staticmethod
    def flat_list(lst, type_to_flat=(list, set)):
        result = []
        for i in lst:
            if isinstance(i, type_to_flat):
                result.extend(Iterable.flat_list(list(i)))
            else:
                result.append(i)
        return result
    @staticmethod
    def search_iterable(iterable, search_with, ignore_case=True):
        result = []
        for o in iterable:
            if ignore_case:
                if str(search_with).lower() in str(o).lower():
                    result.append(o)
            else:
                if str(search_with) in str(o):
                    result.append(o)
        return result
    @staticmethod
    def numred(iterable):
        """numred the objects in an iterable ex: if you want to create numred tasks
            numred(['visiting my uncle', 'water the plants'])  1.visiting my uncle"""
        result = ''
        for i in range(len(iterable)):
            result += f"{i+1}. {iterable[i]}\n"
        return result.strip()
    @staticmethod
    def indexes(iterable, obj):
        return [i for i in range(len(iterable)) if iterable[i] == obj]
    @staticmethod
    def replace_iterable(iterable, index, new_obj=None):
        """replace an object by it's index with new_obj ex:    replace(['mike', 'mark'], 1, 'Olivia')
result = ['Olivia', 'mark']"""
        co = iterable.copy()
        if new_obj:
            co[index-1] = new_obj
        else:
            co.remove(co[index-1])
        return co
    @staticmethod
    def all_any_in(main_iterable, iterable, any_all=all):
        """Checks if all unique elements of 'iterable' exist within 'main_iterable'."""
        if any_all == any:
            for i in set(iterable):
                if i in set(main_iterable):
                    return True
        else:
            return set(iterable).issubset(set(main_iterable))
    @staticmethod
    class Dict:
        def multy_key(dic):
            result = {}
            values = set(dic.values())
            for i in values:
                keys = [o for o in dic if dic[o] == i]
                result[str(keys)] = i
            return result
        def swap_dict(dic):
            """k: v ➡ v, k"""
            result = {}
            for k, v in dic.items():
                if isinstance(v, (list, tuple, set, dict)):
                    v = str(v)
                result[v] = k
            return result
        def return_dict_in_lines(dec):
            """Return a dict formatted as 'key: value' lines."""
            result = ''
            for i in dec:
                result += f"{i}: {dec[i]}\n"
            return result.strip()
class Math:
    @staticmethod
    def int_or_float(num):
        try:
            num = str(num).strip()
            float(num)
            assert num[-1] != '.'
            return True
        except:
            return False
    def iter_num(iterable):
        """Return sum, average, max, and min of an iterable as a dict."""
        return {'sum': sum(iterable), 'average': sum(iterable) / len(iterable), 'max': max(iterable), 'min': min(iterable)}
    @staticmethod
    def arrays(array, step, show='lists'):
        """Split a range into consecutive [start, end] pairs by step.
        If show != 'lists', return a formatted string instead."""
        result = []
        for i in range(step, array, step):
            result.append([i, i+step])
        if show != 'lists':
            result2 = ''
            for i, e in result:
                result2 += str((i, e)).replace('(', '').replace(')', '').replace(', ', ' - ')+'\n'
            return result2.strip()
        return result
