import customtkinter as ctk
from tkinter import messagebox
from pymongo import MongoClient

# --- CONFIGURACIÓN DE APARIENCIA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- CONEXIÓN A MONGODB ---
try:
    client = MongoClient('localhost', 27017)
    db = client['bd_proyecto_parcial2']
    col_project    = db['Project']
    col_department = db['Department']
    col_employee   = db['Employee']
    col_dept_loc   = db['Dept_Locations']
    col_works_on   = db['Works_On']
    col_dependent  = db['Dependent']
except Exception as e:
    messagebox.showerror("Error de Conexión", f"No se pudo conectar a MongoDB: {e}")

SEP = "- " * 17 + "\n\n"

# --- UTILIDADES ---

def limpiar_campos(*campos):
    for campo in campos:
        campo.delete(0, "end")

def validar_campos(campos_dict):
    """Recibe dict {nombre_campo: valor}. Retorna True si todos tienen valor."""
    for nombre, valor in campos_dict.items():
        if not valor.strip():
            messagebox.showwarning("Campo requerido", f"El campo '{nombre}' no puede estar vacío.")
            return False
    return True

def confirmar_baja(nombre):
    return messagebox.askyesno("Confirmar baja", f"¿Estás seguro de que deseas eliminar este registro de {nombre}?")

def exito(operacion, entidad):
    messagebox.showinfo("Operación exitosa", f"{entidad} {operacion} correctamente.")

# --- FUNCIONES CRUD ---

# --- PROJECT ---
def alta_proy():
    campos = {"Número de Proyecto": ent_pnum.get(), "Nombre": ent_pname.get(),
               "Ubicación": ent_ploc.get(), "Número de Departamento": ent_dnum_p.get()}
    if not validar_campos(campos): return
    try:
        # Validación de ID duplicado
        if col_project.find_one({"Pnumber": int(ent_pnum.get())}):
            messagebox.showerror("Error", "El número de proyecto ya existe.")
            return

        col_project.insert_one({
            "Pnumber": int(ent_pnum.get()), "Pname": ent_pname.get().upper(),
            "Plocation": ent_ploc.get().upper(), "Dnum": int(ent_dnum_p.get())
        })
        consulta_proy()
        limpiar_campos(ent_pnum, ent_pname, ent_ploc, ent_dnum_p)
        exito("registrado", "Proyecto")
    except ValueError: messagebox.showerror("Error de Formato", "El número de proyecto y el número de departamento deben ser números.")
    except Exception as e: messagebox.showerror("Error", str(e))

def mod_proy():
    campos = {"Número de Proyecto": ent_pnum.get()}
    if not validar_campos(campos): return
    try:
        col_project.update_one(
            {"Pnumber": int(ent_pnum.get())},
            {"$set": {"Pname": ent_pname.get().upper(), "Plocation": ent_ploc.get().upper(), "Dnum": int(ent_dnum_p.get())}}
        )
        consulta_proy()
        limpiar_campos(ent_pnum, ent_pname, ent_ploc, ent_dnum_p)
        exito("modificado", "Proyecto")
    except ValueError: messagebox.showerror("Error de Formato", "Verifica que los números sean correctos.")
    except Exception as e: messagebox.showerror("Error", str(e))

def baja_proy():
    if not validar_campos({"Número de Proyecto": ent_pnum.get()}): return
    if not confirmar_baja("Proyecto"): return
    try:
        col_project.delete_one({"Pnumber": int(ent_pnum.get())})
        consulta_proy()
        limpiar_campos(ent_pnum, ent_pname, ent_ploc, ent_dnum_p)
        exito("eliminado", "Proyecto")
    except ValueError: messagebox.showerror("Error", "Ingresa un número de proyecto válido.")

def consulta_proy():
    txt_proy.configure(state="normal")
    txt_proy.delete("1.0", "end")
    for p in col_project.find():
        txt_proy.insert("end", f"Proyecto #{p.get('Pnumber', '-')}\n")
        txt_proy.insert("end", f"  Nombre:       {p.get('Pname', '-')}\n")
        txt_proy.insert("end", f"  Ubicación:    {p.get('Plocation', '-')}\n")
        txt_proy.insert("end", f"  Departamento: {p.get('Dnum', '-')}\n")
        txt_proy.insert("end", SEP)
    txt_proy.configure(state="disabled")

def cargar_proy(event):
    idx = txt_proy.index("@%d,%d" % (event.x, event.y))
    linea = int(idx.split(".")[0])
    contenido = txt_proy.get("1.0", "end").split("\n")
    bloque_inicio = linea - 1
    while bloque_inicio > 0 and not contenido[bloque_inicio].startswith("Proyecto #"):
        bloque_inicio -= 1
    if bloque_inicio < len(contenido) and contenido[bloque_inicio].startswith("Proyecto #"):
        try:
            pnum = contenido[bloque_inicio].replace("Proyecto #", "").strip()
            p = col_project.find_one({"Pnumber": int(pnum)})
            if p:
                limpiar_campos(ent_pnum, ent_pname, ent_ploc, ent_dnum_p)
                ent_pnum.insert(0, p.get("Pnumber", ""))
                ent_pname.insert(0, p.get("Pname", ""))
                ent_ploc.insert(0, p.get("Plocation", ""))
                ent_dnum_p.insert(0, p.get("Dnum", ""))
        except: pass

# --- DEPARTMENT ---
def alta_dept():
    campos = {"Número de Departamento": ent_dnumber.get(), "Nombre": ent_dname.get(),
               "NSS del Gerente": ent_mgr_ssn.get(), "Fecha de Inicio": ent_mgr_date.get()}
    if not validar_campos(campos): return
    try:
        # Validación de ID duplicado (REQUERIDO POR EL USUARIO)
        if col_department.find_one({"Dnumber": int(ent_dnumber.get())}):
            messagebox.showerror("Error", "El número de departamento ya existe.")
            return

        col_department.insert_one({
            "Dnumber": int(ent_dnumber.get()), "Dname": ent_dname.get().upper(),
            "Mgr_ssn": ent_mgr_ssn.get(), "Mgr_start_date": ent_mgr_date.get()
        })
        consulta_dept()
        limpiar_campos(ent_dnumber, ent_dname, ent_mgr_ssn, ent_mgr_date)
        exito("registrado", "Departamento")
    except ValueError: messagebox.showerror("Error de Formato", "El número de departamento debe ser un número.")
    except Exception as e: messagebox.showerror("Error", str(e))

def mod_dept():
    if not validar_campos({"Número de Departamento": ent_dnumber.get()}): return
    try:
        col_department.update_one(
            {"Dnumber": int(ent_dnumber.get())},
            {"$set": {"Dname": ent_dname.get().upper(), "Mgr_ssn": ent_mgr_ssn.get(), "Mgr_start_date": ent_mgr_date.get()}}
        )
        consulta_dept()
        limpiar_campos(ent_dnumber, ent_dname, ent_mgr_ssn, ent_mgr_date)
        exito("modificado", "Departamento")
    except ValueError: messagebox.showerror("Error de Formato", "El número de departamento debe ser un número.")
    except Exception as e: messagebox.showerror("Error", str(e))

def baja_dept():
    if not validar_campos({"Número de Departamento": ent_dnumber.get()}): return
    try:
        dnumber = int(ent_dnumber.get())
        empleados = col_employee.count_documents({"Dno": dnumber})
        if empleados > 0:
            messagebox.showerror("Error de Integridad",
                f"No se puede eliminar: el departamento {dnumber} tiene {empleados} empleado(s) asignado(s).")
            return
        if not confirmar_baja("Departamento"): return
        col_department.delete_one({"Dnumber": dnumber})
        consulta_dept()
        limpiar_campos(ent_dnumber, ent_dname, ent_mgr_ssn, ent_mgr_date)
        exito("eliminado", "Departamento")
    except ValueError: messagebox.showerror("Error", "Ingresa un número de departamento válido.")

def consulta_dept():
    txt_dept.configure(state="normal")
    txt_dept.delete("1.0", "end")
    for d in col_department.find():
        txt_dept.insert("end", f"Departamento #{d.get('Dnumber', '-')}\n")
        txt_dept.insert("end", f"  Nombre:               {d.get('Dname', '-')}\n")
        txt_dept.insert("end", f"  NSS del Gerente:      {d.get('Mgr_ssn', '-')}\n")
        txt_dept.insert("end", f"  Fecha Inicio Gerente: {d.get('Mgr_start_date', '-')}\n")
        txt_dept.insert("end", SEP)
    txt_dept.configure(state="disabled")

def cargar_dept(event):
    idx = txt_dept.index("@%d,%d" % (event.x, event.y))
    linea = int(idx.split(".")[0])
    contenido = txt_dept.get("1.0", "end").split("\n")
    bloque_inicio = linea - 1
    while bloque_inicio > 0 and not contenido[bloque_inicio].startswith("Departamento #"):
        bloque_inicio -= 1
    if bloque_inicio < len(contenido) and contenido[bloque_inicio].startswith("Departamento #"):
        try:
            dnum = contenido[bloque_inicio].replace("Departamento #", "").strip()
            d = col_department.find_one({"Dnumber": int(dnum)})
            if d:
                limpiar_campos(ent_dnumber, ent_dname, ent_mgr_ssn, ent_mgr_date)
                ent_dnumber.insert(0, d.get("Dnumber", ""))
                ent_dname.insert(0, d.get("Dname", ""))
                ent_mgr_ssn.insert(0, d.get("Mgr_ssn", ""))
                ent_mgr_date.insert(0, d.get("Mgr_start_date", ""))
        except: pass

# --- EMPLOYEE ---
def alta_emp():
    campos = {"NSS": ent_ssn.get(), "Nombre": ent_fname.get(), "Apellido": ent_lname.get(),
               "Fecha de Nacimiento": ent_bdate.get(), "Dirección": ent_address.get(),
               "Sexo": ent_sex.get(), "Salario": ent_salary.get(), "Número de Departamento": ent_dno.get()}
    if not validar_campos(campos): return
    try:
        # Validación de NSS duplicado
        if col_employee.find_one({"Ssn": ent_ssn.get()}):
            messagebox.showerror("Error", "El NSS ya está registrado para otro empleado.")
            return

        super_ssn_val = ent_super_ssn.get() if ent_super_ssn.get() else None
        col_employee.insert_one({
            "Ssn": ent_ssn.get(), "Fname": ent_fname.get().upper(), "Minit": ent_minit.get().upper(),
            "Lname": ent_lname.get().upper(), "Bdate": ent_bdate.get(), "Address": ent_address.get(),
            "Sex": ent_sex.get().upper(), "Salary": float(ent_salary.get()),
            "Super_ssn": super_ssn_val, "Dno": int(ent_dno.get())
        })
        consulta_emp()
        limpiar_campos(ent_ssn, ent_fname, ent_minit, ent_lname, ent_bdate, ent_address, ent_sex, ent_salary, ent_super_ssn, ent_dno)
        exito("registrado", "Empleado")
    except ValueError: messagebox.showerror("Error de Formato", "El salario y el número de departamento deben ser numéricos.")
    except Exception as e: messagebox.showerror("Error", str(e))

def mod_emp():
    if not validar_campos({"NSS": ent_ssn.get()}): return
    try:
        super_ssn_val = ent_super_ssn.get() if ent_super_ssn.get() else None
        col_employee.update_one(
            {"Ssn": ent_ssn.get()},
            {"$set": {
                "Fname": ent_fname.get().upper(), "Minit": ent_minit.get().upper(),
                "Lname": ent_lname.get().upper(), "Bdate": ent_bdate.get(),
                "Address": ent_address.get(), "Sex": ent_sex.get().upper(),
                "Salary": float(ent_salary.get()), "Super_ssn": super_ssn_val, "Dno": int(ent_dno.get())
            }}
        )
        consulta_emp()
        limpiar_campos(ent_ssn, ent_fname, ent_minit, ent_lname, ent_bdate, ent_address, ent_sex, ent_salary, ent_super_ssn, ent_dno)
        exito("modificado", "Empleado")
    except ValueError: messagebox.showerror("Error de Formato", "El salario y el número de departamento deben ser numéricos.")
    except Exception as e: messagebox.showerror("Error", str(e))

def baja_emp():
    if not validar_campos({"NSS": ent_ssn.get()}): return
    if not confirmar_baja("Empleado"): return
    try:
        col_employee.delete_one({"Ssn": ent_ssn.get()})
        consulta_emp()
        limpiar_campos(ent_ssn, ent_fname, ent_minit, ent_lname, ent_bdate, ent_address, ent_sex, ent_salary, ent_super_ssn, ent_dno)
        exito("eliminado", "Empleado")
    except Exception as e: messagebox.showerror("Error", str(e))

def consulta_emp():
    txt_emp.configure(state="normal")
    txt_emp.delete("1.0", "end")
    for e in col_employee.find():
        txt_emp.insert("end", f"Empleado: {e.get('Fname','')} {e.get('Minit','')}. {e.get('Lname','')}\n")
        txt_emp.insert("end", f"  NSS:            {e.get('Ssn', '-')}\n")
        txt_emp.insert("end", f"  Fecha Nac.:     {e.get('Bdate', '-')}\n")
        txt_emp.insert("end", f"  Dirección:      {e.get('Address', '-')}\n")
        txt_emp.insert("end", f"  Sexo:           {e.get('Sex', '-')}\n")
        txt_emp.insert("end", f"  Salario:        ${e.get('Salary', '-')}\n")
        txt_emp.insert("end", f"  NSS Supervisor: {e.get('Super_ssn', 'N/A')}\n")
        dept = col_department.find_one({"Dnumber": e.get("Dno")})
        nombre_dept = dept.get("Dname", "-") if dept else f"#{e.get('Dno', '-')} (no encontrado)"
        txt_emp.insert("end", f"  Departamento:    {nombre_dept}\n")
        txt_emp.insert("end", SEP)
    txt_emp.configure(state="disabled")

def cargar_emp(event):
    idx = txt_emp.index("@%d,%d" % (event.x, event.y))
    linea = int(idx.split(".")[0])
    contenido = txt_emp.get("1.0", "end").split("\n")
    bloque_inicio = linea - 1
    while bloque_inicio > 0 and not contenido[bloque_inicio].startswith("Empleado:"):
        bloque_inicio -= 1
    if bloque_inicio < len(contenido) and contenido[bloque_inicio].startswith("Empleado:"):
        try:
            ssn = ""
            for i in range(bloque_inicio, min(bloque_inicio + 10, len(contenido))):
                if "NSS:" in contenido[i]:
                    ssn = contenido[i].replace("NSS:", "").replace(" ", "").strip()
                    break
            e = col_employee.find_one({"Ssn": ssn})
            if e:
                limpiar_campos(ent_ssn, ent_fname, ent_minit, ent_lname, ent_bdate, ent_address, ent_sex, ent_salary, ent_super_ssn, ent_dno)
                ent_ssn.insert(0, e.get("Ssn", ""))
                ent_fname.insert(0, e.get("Fname", ""))
                ent_minit.insert(0, e.get("Minit", ""))
                ent_lname.insert(0, e.get("Lname", ""))
                ent_bdate.insert(0, e.get("Bdate", ""))
                ent_address.insert(0, e.get("Address", ""))
                ent_sex.insert(0, e.get("Sex", ""))
                ent_salary.insert(0, e.get("Salary", ""))
                ent_super_ssn.insert(0, e.get("Super_ssn", "") or "")
                ent_dno.insert(0, e.get("Dno", ""))
        except: pass

# --- DEPT_LOCATIONS ---
def alta_dept_loc():
    campos = {"Número de Departamento": ent_dl_num.get(), "Ubicación": ent_dl_loc.get()}
    if not validar_campos(campos): return
    try:
        # Validación de Duplicado (Clave compuesta Dnumber + Dlocation)
        if col_dept_loc.find_one({"Dnumber": int(ent_dl_num.get()), "Dlocation": ent_dl_loc.get().upper()}):
            messagebox.showerror("Error", "Esta ubicación ya existe para este departamento.")
            return

        col_dept_loc.insert_one({"Dnumber": int(ent_dl_num.get()), "Dlocation": ent_dl_loc.get().upper()})
        consulta_dept_loc()
        limpiar_campos(ent_dl_num, ent_dl_loc)
        exito("registrada", "Ubicación")
    except ValueError: messagebox.showerror("Error de Formato", "El número de departamento debe ser numérico.")
    except Exception as e: messagebox.showerror("Error", str(e))

def mod_dept_loc():
    if not validar_campos({"Número de Departamento": ent_dl_num.get()}): return
    try:
        col_dept_loc.update_one(
            {"Dnumber": int(ent_dl_num.get())},
            {"$set": {"Dlocation": ent_dl_loc.get().upper()}}
        )
        consulta_dept_loc()
        limpiar_campos(ent_dl_num, ent_dl_loc)
        exito("modificada", "Ubicación")
    except ValueError: messagebox.showerror("Error de Formato", "El número de departamento debe ser numérico.")
    except Exception as e: messagebox.showerror("Error", str(e))

def baja_dept_loc():
    if not validar_campos({"Número de Departamento": ent_dl_num.get(), "Ubicación": ent_dl_loc.get()}): return
    if not confirmar_baja("Ubicación"): return
    try:
        col_dept_loc.delete_one({"Dnumber": int(ent_dl_num.get()), "Dlocation": ent_dl_loc.get().upper()})
        consulta_dept_loc()
        limpiar_campos(ent_dl_num, ent_dl_loc)
        exito("eliminada", "Ubicación")
    except ValueError: messagebox.showerror("Error", "Ingresa un número de departamento válido.")

def consulta_dept_loc():
    txt_dept_loc.configure(state="normal")
    txt_dept_loc.delete("1.0", "end")
    for dl in col_dept_loc.find():
        txt_dept_loc.insert("end", f"Departamento #{dl.get('Dnumber', '-')}\n")
        txt_dept_loc.insert("end", f"  Ubicación: {dl.get('Dlocation', '-')}\n")
        txt_dept_loc.insert("end", SEP)
    txt_dept_loc.configure(state="disabled")

def cargar_dept_loc(event):
    idx = txt_dept_loc.index("@%d,%d" % (event.x, event.y))
    linea = int(idx.split(".")[0])
    contenido = txt_dept_loc.get("1.0", "end").split("\n")
    bloque_inicio = linea - 1
    while bloque_inicio > 0 and not contenido[bloque_inicio].startswith("Departamento #"):
        bloque_inicio -= 1
    if bloque_inicio < len(contenido) and contenido[bloque_inicio].startswith("Departamento #"):
        try:
            dnum = contenido[bloque_inicio].replace("Departamento #", "").strip()
            dloc = ""
            if bloque_inicio + 1 < len(contenido):
                dloc = contenido[bloque_inicio + 1].replace("Ubicación:", "").strip()
            limpiar_campos(ent_dl_num, ent_dl_loc)
            ent_dl_num.insert(0, dnum)
            ent_dl_loc.insert(0, dloc)
        except: pass

# --- WORKS_ON ---
def alta_works_on():
    campos = {"NSS del Empleado": ent_wo_essn.get(), "Número de Proyecto": ent_wo_pno.get(), "Horas Trabajadas": ent_wo_hours.get()}
    if not validar_campos(campos): return
    try:
        # Validación de Duplicado
        if col_works_on.find_one({"Essn": ent_wo_essn.get(), "Pno": int(ent_wo_pno.get())}):
            messagebox.showerror("Error", "Esta asignación de empleado a proyecto ya existe.")
            return

        col_works_on.insert_one({"Essn": ent_wo_essn.get(), "Pno": int(ent_wo_pno.get()), "Hours": float(ent_wo_hours.get())})
        consulta_works_on()
        limpiar_campos(ent_wo_essn, ent_wo_pno, ent_wo_hours)
        exito("registrada", "Asignación")
    except ValueError: messagebox.showerror("Error de Formato", "El número de proyecto y las horas deben ser numéricos.")
    except Exception as e: messagebox.showerror("Error", str(e))

def mod_works_on():
    if not validar_campos({"NSS del Empleado": ent_wo_essn.get(), "Número de Proyecto": ent_wo_pno.get()}): return
    try:
        col_works_on.update_one(
            {"Essn": ent_wo_essn.get(), "Pno": int(ent_wo_pno.get())},
            {"$set": {"Hours": float(ent_wo_hours.get())}}
        )
        consulta_works_on()
        limpiar_campos(ent_wo_essn, ent_wo_pno, ent_wo_hours)
        exito("modificada", "Asignación")
    except ValueError: messagebox.showerror("Error de Formato", "El número de proyecto y las horas deben ser numéricos.")
    except Exception as e: messagebox.showerror("Error", str(e))

def baja_works_on():
    if not validar_campos({"NSS del Empleado": ent_wo_essn.get(), "Número de Proyecto": ent_wo_pno.get()}): return
    if not confirmar_baja("Asignación"): return
    try:
        col_works_on.delete_one({"Essn": ent_wo_essn.get(), "Pno": int(ent_wo_pno.get())})
        consulta_works_on()
        limpiar_campos(ent_wo_essn, ent_wo_pno, ent_wo_hours)
        exito("eliminada", "Asignación")
    except ValueError: messagebox.showerror("Error", "Ingresa un número de proyecto válido.")

def consulta_works_on():
    txt_wo.configure(state="normal")
    txt_wo.delete("1.0", "end")
    for w in col_works_on.find():
        horas = w.get('Hours', '-')
        txt_wo.insert("end", f"NSS Empleado:  {w.get('Essn', '-')}\n")
        txt_wo.insert("end", f"  Proyecto #:  {w.get('Pno', '-')}\n")
        txt_wo.insert("end", f"  Horas Trab.: {horas if horas is not None else 'N/A'}\n")
        txt_wo.insert("end", SEP)
    txt_wo.configure(state="disabled")

def cargar_works_on(event):
    idx = txt_wo.index("@%d,%d" % (event.x, event.y))
    linea = int(idx.split(".")[0])
    contenido = txt_wo.get("1.0", "end").split("\n")
    bloque_inicio = linea - 1
    while bloque_inicio > 0 and not contenido[bloque_inicio].startswith("NSS Empleado:"):
        bloque_inicio -= 1
    if bloque_inicio < len(contenido) and contenido[bloque_inicio].startswith("NSS Empleado:"):
        try:
            essn = contenido[bloque_inicio].replace("NSS Empleado:", "").strip()
            pno  = contenido[bloque_inicio + 1].replace("Proyecto #:", "").replace(" ", "").strip()
            horas = contenido[bloque_inicio + 2].replace("Horas Trab.:", "").replace(" ", "").strip()
            limpiar_campos(ent_wo_essn, ent_wo_pno, ent_wo_hours)
            ent_wo_essn.insert(0, essn)
            ent_wo_pno.insert(0, pno)
            ent_wo_hours.insert(0, "" if horas == "N/A" else horas)
        except: pass

# --- DEPENDENT ---
def alta_dep():
    campos = {"NSS del Empleado": ent_dep_essn.get(), "Nombre del Dependiente": ent_dep_name.get(),
               "Sexo": ent_dep_sex.get(), "Fecha de Nacimiento": ent_dep_bdate.get(), "Parentesco": ent_dep_rel.get()}
    if not validar_campos(campos): return
    try:
        # Validación de Duplicado
        if col_dependent.find_one({"Essn": ent_dep_essn.get(), "Dependent_name": ent_dep_name.get().upper()}):
            messagebox.showerror("Error", "Este dependiente ya está registrado para este empleado.")
            return

        col_dependent.insert_one({
            "Essn": ent_dep_essn.get(), "Dependent_name": ent_dep_name.get().upper(),
            "Sex": ent_dep_sex.get().upper(), "Bdate": ent_dep_bdate.get(), "Relationship": ent_dep_rel.get().upper()
        })
        consulta_dep()
        limpiar_campos(ent_dep_essn, ent_dep_name, ent_dep_sex, ent_dep_bdate, ent_dep_rel)
        exito("registrado", "Dependiente")
    except Exception as e: messagebox.showerror("Error", str(e))

def mod_dep():
    if not validar_campos({"NSS del Empleado": ent_dep_essn.get(), "Nombre del Dependiente": ent_dep_name.get()}): return
    try:
        col_dependent.update_one(
            {"Essn": ent_dep_essn.get(), "Dependent_name": ent_dep_name.get().upper()},
            {"$set": {"Sex": ent_dep_sex.get().upper(), "Bdate": ent_dep_bdate.get(), "Relationship": ent_dep_rel.get().upper()}}
        )
        consulta_dep()
        limpiar_campos(ent_dep_essn, ent_dep_name, ent_dep_sex, ent_dep_bdate, ent_dep_rel)
        exito("modificado", "Dependiente")
    except Exception as e: messagebox.showerror("Error", str(e))

def baja_dep():
    if not validar_campos({"NSS del Empleado": ent_dep_essn.get(), "Nombre del Dependiente": ent_dep_name.get()}): return
    if not confirmar_baja("Dependiente"): return
    try:
        col_dependent.delete_one({"Essn": ent_dep_essn.get(), "Dependent_name": ent_dep_name.get().upper()})
        consulta_dep()
        limpiar_campos(ent_dep_essn, ent_dep_name, ent_dep_sex, ent_dep_bdate, ent_dep_rel)
        exito("eliminado", "Dependiente")
    except Exception as e: messagebox.showerror("Error", str(e))

def consulta_dep():
    txt_dep.configure(state="normal")
    txt_dep.delete("1.0", "end")
    for dp in col_dependent.find():
        txt_dep.insert("end", f"Dependiente: {dp.get('Dependent_name', '-')}\n")
        txt_dep.insert("end", f"  NSS Empleado: {dp.get('Essn', '-')}\n")
        txt_dep.insert("end", f"  Sexo:         {dp.get('Sex', '-')}\n")
        txt_dep.insert("end", f"  Fecha Nac.:   {dp.get('Bdate', '-')}\n")
        txt_dep.insert("end", f"  Parentesco:   {dp.get('Relationship', '-')}\n")
        txt_dep.insert("end", SEP)
    txt_dep.configure(state="disabled")

def cargar_dep(event):
    idx = txt_dep.index("@%d,%d" % (event.x, event.y))
    linea = int(idx.split(".")[0])
    contenido = txt_dep.get("1.0", "end").split("\n")
    bloque_inicio = linea - 1
    while bloque_inicio > 0 and not contenido[bloque_inicio].startswith("Dependiente:"):
        bloque_inicio -= 1
    if bloque_inicio < len(contenido) and contenido[bloque_inicio].startswith("Dependiente:"):
        try:
            nombre = contenido[bloque_inicio].replace("Dependiente:", "").strip()
            essn   = contenido[bloque_inicio + 1].replace("NSS Empleado:", "").strip()
            sexo   = contenido[bloque_inicio + 2].replace("Sexo:", "").strip()
            bdate  = contenido[bloque_inicio + 3].replace("Fecha Nac.:", "").strip()
            rel    = contenido[bloque_inicio + 4].replace("Parentesco:", "").strip()
            limpiar_campos(ent_dep_essn, ent_dep_name, ent_dep_sex, ent_dep_bdate, ent_dep_rel)
            ent_dep_essn.insert(0, essn)
            ent_dep_name.insert(0, nombre)
            ent_dep_sex.insert(0, sexo)
            ent_dep_bdate.insert(0, bdate)
            ent_dep_rel.insert(0, rel)
        except: pass

# --- INTERFAZ GRÁFICA ---
app = ctk.CTk()
app.title("Sistema Empresa - bd_proyectoparcial2")
app.geometry("950x650")

tabs = ctk.CTkTabview(app, width=900, height=600)
tabs.pack(padx=10, pady=10)

t_p   = tabs.add("Proyectos")
t_d   = tabs.add("Departamentos")
t_e   = tabs.add("Empleados")
t_dl  = tabs.add("Ubicaciones")
t_w   = tabs.add("Asignaciones")
t_dep = tabs.add("Dependientes")

# --- UI: PROJECT ---
f1 = ctk.CTkFrame(t_p, fg_color="transparent"); f1.pack(side="left", padx=10)
ctk.CTkLabel(f1, text="Número de Proyecto:").pack();     ent_pnum   = ctk.CTkEntry(f1); ent_pnum.pack()
ctk.CTkLabel(f1, text="Nombre del Proyecto:").pack();    ent_pname  = ctk.CTkEntry(f1); ent_pname.pack()
ctk.CTkLabel(f1, text="Ubicación:").pack();              ent_ploc   = ctk.CTkEntry(f1); ent_ploc.pack()
ctk.CTkLabel(f1, text="Número de Departamento:").pack(); ent_dnum_p = ctk.CTkEntry(f1); ent_dnum_p.pack()
f2 = ctk.CTkFrame(t_p, fg_color="transparent"); f2.pack(side="left", padx=10)
ctk.CTkButton(f2, text="Alta",      fg_color="green",   command=alta_proy).pack(pady=5)
ctk.CTkButton(f2, text="Modificar", fg_color="#d48c00", command=mod_proy).pack(pady=5)
ctk.CTkButton(f2, text="Baja",      fg_color="red",     command=baja_proy).pack(pady=5)
ctk.CTkButton(f2, text="Limpiar",   fg_color="gray",    command=lambda: limpiar_campos(ent_pnum, ent_pname, ent_ploc, ent_dnum_p)).pack(pady=5)
txt_proy = ctk.CTkTextbox(t_p, width=400); txt_proy.pack(side="right", padx=10, pady=10)
txt_proy.bind("<Button-1>", cargar_proy)

# --- UI: DEPARTMENT ---
fd1 = ctk.CTkFrame(t_d, fg_color="transparent"); fd1.pack(side="left", padx=10)
ctk.CTkLabel(fd1, text="Número de Departamento:").pack();    ent_dnumber  = ctk.CTkEntry(fd1); ent_dnumber.pack()
ctk.CTkLabel(fd1, text="Nombre del Departamento:").pack();   ent_dname    = ctk.CTkEntry(fd1); ent_dname.pack()
ctk.CTkLabel(fd1, text="NSS del Gerente:").pack();           ent_mgr_ssn  = ctk.CTkEntry(fd1); ent_mgr_ssn.pack()
ctk.CTkLabel(fd1, text="Fecha de Inicio del Gerente:").pack(); ent_mgr_date = ctk.CTkEntry(fd1); ent_mgr_date.pack()
fd2 = ctk.CTkFrame(t_d, fg_color="transparent"); fd2.pack(side="left", padx=10)
ctk.CTkButton(fd2, text="Alta",      fg_color="green",   command=alta_dept).pack(pady=5)
ctk.CTkButton(fd2, text="Modificar", fg_color="#d48c00", command=mod_dept).pack(pady=5)
ctk.CTkButton(fd2, text="Baja",      fg_color="red",     command=baja_dept).pack(pady=5)
ctk.CTkButton(fd2, text="Limpiar",   fg_color="gray",    command=lambda: limpiar_campos(ent_dnumber, ent_dname, ent_mgr_ssn, ent_mgr_date)).pack(pady=5)
txt_dept = ctk.CTkTextbox(t_d, width=400); txt_dept.pack(side="right", padx=10, pady=10)
txt_dept.bind("<Button-1>", cargar_dept)

# --- UI: EMPLOYEE ---
fe1_a = ctk.CTkFrame(t_e, fg_color="transparent"); fe1_a.pack(side="left", padx=5)
ctk.CTkLabel(fe1_a, text="NSS (Núm. Seguro Social):").pack(); ent_ssn   = ctk.CTkEntry(fe1_a); ent_ssn.pack()
ctk.CTkLabel(fe1_a, text="Nombre:").pack();                   ent_fname = ctk.CTkEntry(fe1_a); ent_fname.pack()
ctk.CTkLabel(fe1_a, text="Inicial Segundo Nombre:").pack();   ent_minit = ctk.CTkEntry(fe1_a); ent_minit.pack()
ctk.CTkLabel(fe1_a, text="Apellido:").pack();                 ent_lname = ctk.CTkEntry(fe1_a); ent_lname.pack()
ctk.CTkLabel(fe1_a, text="Fecha de Nacimiento:").pack();      ent_bdate = ctk.CTkEntry(fe1_a); ent_bdate.pack()
fe1_b = ctk.CTkFrame(t_e, fg_color="transparent"); fe1_b.pack(side="left", padx=5)
ctk.CTkLabel(fe1_b, text="Dirección:").pack();               ent_address   = ctk.CTkEntry(fe1_b); ent_address.pack()
ctk.CTkLabel(fe1_b, text="Sexo (M/F):").pack();               ent_sex       = ctk.CTkEntry(fe1_b); ent_sex.pack()
ctk.CTkLabel(fe1_b, text="Salario:").pack();                  ent_salary    = ctk.CTkEntry(fe1_b); ent_salary.pack()
ctk.CTkLabel(fe1_b, text="NSS del Supervisor:").pack();       ent_super_ssn = ctk.CTkEntry(fe1_b); ent_super_ssn.pack()
ctk.CTkLabel(fe1_b, text="Número de Departamento:").pack();   ent_dno       = ctk.CTkEntry(fe1_b); ent_dno.pack()
fe2 = ctk.CTkFrame(t_e, fg_color="transparent"); fe2.pack(side="left", padx=5)
ctk.CTkButton(fe2, text="Alta",      fg_color="green",   command=alta_emp).pack(pady=5)
ctk.CTkButton(fe2, text="Modificar", fg_color="#d48c00", command=mod_emp).pack(pady=5)
ctk.CTkButton(fe2, text="Baja",      fg_color="red",     command=baja_emp).pack(pady=5)
ctk.CTkButton(fe2, text="Limpiar",   fg_color="gray",    command=lambda: limpiar_campos(ent_ssn, ent_fname, ent_minit, ent_lname, ent_bdate, ent_address, ent_sex, ent_salary, ent_super_ssn, ent_dno)).pack(pady=5)
txt_emp = ctk.CTkTextbox(t_e, width=320); txt_emp.pack(side="right", padx=10, pady=10)
txt_emp.bind("<Button-1>", cargar_emp)

# --- UI: DEPT_LOCATIONS ---
fdl1 = ctk.CTkFrame(t_dl, fg_color="transparent"); fdl1.pack(side="left", padx=10)
ctk.CTkLabel(fdl1, text="Número de Departamento:").pack(); ent_dl_num = ctk.CTkEntry(fdl1); ent_dl_num.pack()
ctk.CTkLabel(fdl1, text="Ubicación:").pack();              ent_dl_loc = ctk.CTkEntry(fdl1); ent_dl_loc.pack()
fdl2 = ctk.CTkFrame(t_dl, fg_color="transparent"); fdl2.pack(side="left", padx=10)
ctk.CTkButton(fdl2, text="Alta",      fg_color="green",   command=alta_dept_loc).pack(pady=5)
ctk.CTkButton(fdl2, text="Modificar", fg_color="#d48c00", command=mod_dept_loc).pack(pady=5)
ctk.CTkButton(fdl2, text="Baja",      fg_color="red",     command=baja_dept_loc).pack(pady=5)
ctk.CTkButton(fdl2, text="Limpiar",   fg_color="gray",    command=lambda: limpiar_campos(ent_dl_num, ent_dl_loc)).pack(pady=5)
txt_dept_loc = ctk.CTkTextbox(t_dl, width=400); txt_dept_loc.pack(side="right", padx=10, pady=10)
txt_dept_loc.bind("<Button-1>", cargar_dept_loc)

# --- UI: WORKS_ON ---
fw1 = ctk.CTkFrame(t_w, fg_color="transparent"); fw1.pack(side="left", padx=10)
ctk.CTkLabel(fw1, text="NSS del Empleado:").pack();   ent_wo_essn  = ctk.CTkEntry(fw1); ent_wo_essn.pack()
ctk.CTkLabel(fw1, text="Número de Proyecto:").pack(); ent_wo_pno   = ctk.CTkEntry(fw1); ent_wo_pno.pack()
ctk.CTkLabel(fw1, text="Horas Trabajadas:").pack();   ent_wo_hours = ctk.CTkEntry(fw1); ent_wo_hours.pack()
fw2 = ctk.CTkFrame(t_w, fg_color="transparent"); fw2.pack(side="left", padx=10)
ctk.CTkButton(fw2, text="Alta",      fg_color="green",   command=alta_works_on).pack(pady=5)
ctk.CTkButton(fw2, text="Modificar", fg_color="#d48c00", command=mod_works_on).pack(pady=5)
ctk.CTkButton(fw2, text="Baja",      fg_color="red",     command=baja_works_on).pack(pady=5)
ctk.CTkButton(fw2, text="Limpiar",   fg_color="gray",    command=lambda: limpiar_campos(ent_wo_essn, ent_wo_pno, ent_wo_hours)).pack(pady=5)
txt_wo = ctk.CTkTextbox(t_w, width=400); txt_wo.pack(side="right", padx=10, pady=10)
txt_wo.bind("<Button-1>", cargar_works_on)

# --- UI: DEPENDENT ---
fdep1 = ctk.CTkFrame(t_dep, fg_color="transparent"); fdep1.pack(side="left", padx=10)
ctk.CTkLabel(fdep1, text="NSS del Empleado:").pack();       ent_dep_essn  = ctk.CTkEntry(fdep1); ent_dep_essn.pack()
ctk.CTkLabel(fdep1, text="Nombre del Dependiente:").pack(); ent_dep_name  = ctk.CTkEntry(fdep1); ent_dep_name.pack()
ctk.CTkLabel(fdep1, text="Sexo (M/F):").pack();             ent_dep_sex   = ctk.CTkEntry(fdep1); ent_dep_sex.pack()
ctk.CTkLabel(fdep1, text="Fecha de Nacimiento:").pack();    ent_dep_bdate = ctk.CTkEntry(fdep1); ent_dep_bdate.pack()
ctk.CTkLabel(fdep1, text="Parentesco:").pack();             ent_dep_rel   = ctk.CTkEntry(fdep1); ent_dep_rel.pack()
fdep2 = ctk.CTkFrame(t_dep, fg_color="transparent"); fdep2.pack(side="left", padx=10)
ctk.CTkButton(fdep2, text="Alta",      fg_color="green",   command=alta_dep).pack(pady=5)
ctk.CTkButton(fdep2, text="Modificar", fg_color="#d48c00", command=mod_dep).pack(pady=5)
ctk.CTkButton(fdep2, text="Baja",      fg_color="red",     command=baja_dep).pack(pady=5)
ctk.CTkButton(fdep2, text="Limpiar",   fg_color="gray",    command=lambda: limpiar_campos(ent_dep_essn, ent_dep_name, ent_dep_sex, ent_dep_bdate, ent_dep_rel)).pack(pady=5)
txt_dep = ctk.CTkTextbox(t_dep, width=400); txt_dep.pack(side="right", padx=10, pady=10)
txt_dep.bind("<Button-1>", cargar_dep)

consulta_proy(); consulta_dept(); consulta_emp(); consulta_dept_loc(); consulta_works_on(); consulta_dep()
app.mainloop()
