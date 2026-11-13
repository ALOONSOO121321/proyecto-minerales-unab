import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PMV - Minerales y Gemas", layout="wide", page_icon="💎")

# ==========================================
# 0. ESTILOS VISUALES TEMÁTICOS Y DISEÑO
# ==========================================
st.markdown("""
    <style>
    /* Fondo degradado original + textura sutil de facetas de cristal/minerales en SVG */
    .stApp {
        background-color: #e6ecf5;
        background-image: 
            url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg stroke='%232980b9' stroke-opacity='0.09' stroke-width='1.2'%3E%3Cpolygon points='40 0 80 20 80 60 40 80 0 60 0 20'/%3E%3Cpolyline points='0 20 40 40 80 20'/%3E%3Cline x1='40' y1='40' x2='40' y2='80'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E"),
            linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        background-attachment: fixed;
    }
    
    /* Banner superior decorativo de minerales */
    .mineral-banner {
        background: linear-gradient(120deg, #1b2631 0%, #2c3e50 60%, #1f618d 100%);
        color: #ffffff;
        padding: 18px 25px;
        border-radius: 14px;
        border-left: 6px solid #5dade2;
        box-shadow: 0 6px 18px rgba(27, 38, 49, 0.18);
        margin-bottom: 20px;
    }
    .mineral-banner h2 {
        margin: 0;
        color: #ffffff;
        font-size: 1.5rem;
    }
    .mineral-banner p {
        margin: 4px 0 0 0;
        color: #d6eaf8;
        font-size: 0.95rem;
    }

    /* Estilo del menú lateral */
    section[data-testid="stSidebar"] {
        background-color: #1b2631;
        color: #ffffff;
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label {
        color: #ecf0f1;
    }

    /* Tarjetas personalizadas estilo cristal/vitrina */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(4px);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
        border: 1px solid #aed6f1;
        border-top: 4px solid #2980b9;
    }

    /* Botones atractivos */
    .stButton>button {
        background: linear-gradient(135deg, #2980b9 0%, #2c3e50 100%);
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        border: none;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(41, 128, 185, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #3498db 0%, #1a252f 100%);
        box-shadow: 0 6px 15px rgba(41, 128, 185, 0.5);
    }

    /* Enlaces de referencia */
    .ref-link {
        font-size: 0.9rem;
        color: #2980b9;
        text-decoration: none;
        font-weight: 600;
    }
    .ref-link:hover {
        text-decoration: underline;
        color: #1b4f72;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. CONTROL DE ACCESO Y ESTADO INICIAL
# ==========================================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.rol = None
    st.session_state.usuario = None

# Catálogo Oficial e Inventario inicial
if "catalogo_piezas" not in st.session_state:
    st.session_state.catalogo_piezas = pd.DataFrame([
        {
            "idPieza": "PZ01", "nombrePieza": "Cuarzo Rosa", "tipoPieza": "Mineral", 
            "idColeccion": "CO01", "nombreColeccion": "Tesoros Andinos", "valorEstimado": 85000,
            "stock": 14, "fuente": "https://geologyscience.com/es/gemstones/rare-unique-gemstones/rose-quartz/"
        },
        {
            "idPieza": "PZ02", "nombrePieza": "Amonite Jurásico", "tipoPieza": "Fósil", 
            "idColeccion": "CO02", "nombreColeccion": "Historia Fósil", "valorEstimado": 130000,
            "stock": 6, "fuente": "https://geologyscience.com/es/fossils/ammonites/"
        },
        {
            "idPieza": "PZ03", "nombrePieza": "Zafiro Azul", "tipoPieza": "Gema", 
            "idColeccion": "CO03", "nombreColeccion": "Gemas del Mundo", "valorEstimado": 320000,
            "stock": 3, "fuente": "https://www.celinni.com/es/content/173-piedra-de-nacimiento-septiembre"
        },
        {
            "idPieza": "PZ04", "nombrePieza": "Pirita Dorada", "tipoPieza": "Mineral", 
            "idColeccion": "CO01", "nombreColeccion": "Tesoros Andinos", "valorEstimado": 65000,
            "stock": 20, "fuente": "https://www.labrujulaverde.com/2021/06/encuentran-que-la-pirita-el-oro-de-los-tontos-si-contiene-pequenas-cantidades-de-oro"
        },
        {
            "idPieza": "PZ05", "nombrePieza": "Trilobite", "tipoPieza": "Fósil", 
            "idColeccion": "CO02", "nombreColeccion": "Historia Fósil", "valorEstimado": 110000,
            "stock": 8, "fuente": "https://fossilcartel.com/product/trilobite-fossil-flexicalymene/"
        }
    ])

if "stock" not in st.session_state.catalogo_piezas.columns:
    st.session_state.catalogo_piezas["stock"] = 10

# Registro Histórico Completo de Ventas
if "ventas_realizadas" not in st.session_state:
    st.session_state.ventas_realizadas = pd.DataFrame([
        {"idDetalleVenta": "DV01", "idCliente": "CL01", "nombreCliente": "Museo Norte", "idPieza": "PZ01", "nombrePieza": "Cuarzo Rosa", "precioventa": 80750, "nombreExposicion": "Mineralia 2026", "notaEva": 3},
        {"idDetalleVenta": "DV02", "idCliente": "CL01", "nombreCliente": "Museo Norte", "idPieza": "PZ02", "nombrePieza": "Amonite Jurásico", "precioventa": 126100, "nombreExposicion": "Mineralia 2026", "notaEva": 4},
        {"idDetalleVenta": "DV03", "idCliente": "CL01", "nombreCliente": "Museo Norte", "idPieza": "PZ03", "nombrePieza": "Zafiro Azul", "precioventa": 316800, "nombreExposicion": "Mineralia 2026", "notaEva": 5},
        {"idDetalleVenta": "DV04", "idCliente": "CL01", "nombreCliente": "Museo Norte", "idPieza": "PZ04", "nombrePieza": "Pirita Dorada", "precioventa": 65650, "nombreExposicion": "Mineralia 2026", "notaEva": 3},
        {"idDetalleVenta": "DV01", "idCliente": "CL02", "nombreCliente": "Patricia Gómez", "idPieza": "PZ02", "nombrePieza": "Amonite Jurásico", "precioventa": 123500, "nombreExposicion": "Expo Fósiles", "notaEva": 4},
        {"idDetalleVenta": "DV02", "idCliente": "CL02", "nombreCliente": "Patricia Gómez", "idPieza": "PZ03", "nombrePieza": "Zafiro Azul", "precioventa": 310400, "nombreExposicion": "Expo Fósiles", "notaEva": 5},
        {"idDetalleVenta": "DV03", "idCliente": "CL02", "nombreCliente": "Patricia Gómez", "idPieza": "PZ04", "nombrePieza": "Pirita Dorada", "precioventa": 64350, "nombreExposicion": "Expo Fósiles", "notaEva": 3},
        {"idDetalleVenta": "DV04", "idCliente": "CL02", "nombreCliente": "Patricia Gómez", "idPieza": "PZ05", "nombrePieza": "Trilobite", "precioventa": 111100, "nombreExposicion": "Expo Fósiles", "notaEva": 4},
        {"idDetalleVenta": "DV01", "idCliente": "CL03", "nombreCliente": "Centro Geológico", "idPieza": "PZ03", "nombrePieza": "Zafiro Azul", "precioventa": 304000, "nombreExposicion": "Gemas Internacional", "notaEva": 5},
        {"idDetalleVenta": "DV02", "idCliente": "CL03", "nombreCliente": "Centro Geológico", "idPieza": "PZ04", "nombrePieza": "Pirita Dorada", "precioventa": 63050, "nombreExposicion": "Gemas Internacional", "notaEva": 3},
        {"idDetalleVenta": "DV03", "idCliente": "CL03", "nombreCliente": "Centro Geológico", "idPieza": "PZ05", "nombrePieza": "Trilobite", "precioventa": 108900, "nombreExposicion": "Gemas Internacional", "notaEva": 4},
        {"idDetalleVenta": "DV04", "idCliente": "CL03", "nombreCliente": "Centro Geológico", "idPieza": "PZ01", "nombrePieza": "Cuarzo Rosa", "precioventa": 85850, "nombreExposicion": "Gemas Internacional", "notaEva": 5},
        {"idDetalleVenta": "DV01", "idCliente": "CL04", "nombreCliente": "Diego Vera", "idPieza": "PZ04", "nombrePieza": "Pirita Dorada", "precioventa": 61750, "nombreExposicion": "Mineralia 2026", "notaEva": 3},
        {"idDetalleVenta": "DV02", "idCliente": "CL04", "nombreCliente": "Diego Vera", "idPieza": "PZ05", "nombrePieza": "Trilobite", "precioventa": 106700, "nombreExposicion": "Mineralia 2026", "notaEva": 4},
        {"idDetalleVenta": "DV03", "idCliente": "CL04", "nombreCliente": "Diego Vera", "idPieza": "PZ01", "nombrePieza": "Cuarzo Rosa", "precioventa": 84150, "nombreExposicion": "Mineralia 2026", "notaEva": 5},
        {"idDetalleVenta": "DV04", "idCliente": "CL04", "nombreCliente": "Diego Vera", "idPieza": "PZ02", "nombrePieza": "Amonite Jurásico", "precioventa": 131300, "nombreExposicion": "Mineralia 2026", "notaEva": 3}
    ])

st.sidebar.markdown("## 💎🪨 GeoGemas PMV")
st.sidebar.caption("Sistema de Gestión Mineralógica")
st.sidebar.markdown("---")
st.sidebar.title("🔐 Acceso al Sistema")

if not st.session_state.autenticado:
    with st.sidebar.form("login_form"):
        user_input = st.text_input("Usuario")
        pass_input = st.text_input("Contraseña", type="password")
        btn_login = st.form_submit_button("Iniciar Sesión")
        
        if btn_login:
            if user_input == "admin" and pass_input == "1234":
                st.session_state.autenticado = True
                st.session_state.rol = "Administrador"
                st.session_state.usuario = "Administrador General"
                st.rerun()
            elif user_input == "gestor" and pass_input == "1234":
                st.session_state.autenticado = True
                st.session_state.rol = "Gestor Comercial"
                st.session_state.usuario = "Gestor de Ventas"
                st.rerun()
            else:
                st.error("Credenciales inválidas. Pruebe: admin/1234 o gestor/1234")
    st.info("👈 Inicie sesión en el menú lateral para operar el PMV.")
    st.stop()
else:
    st.sidebar.success(f"Usuario: **{st.session_state.usuario}**\n\nRol: **{st.session_state.rol}**")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.clear()
        st.rerun()

menu = st.sidebar.radio("Navegación", [
    "🏠 Inicio", 
    "📋 Registro de Ventas", 
    "💎 Catálogo", 
    "📦 Inventario",
    "🛒 Registrador de Ventas", 
    "➕ Registrador de Minerales"
])

# Banner superior temático
st.markdown("""
    <div class="mineral-banner">
        <h2>💎🪨 Colección & Gestión de Minerales, Gemas y Fósiles ✨</h2>
        <p>Plataforma de control geológico, exhibición de especímenes y administración comercial</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 2. VISTAS DE LA APLICACIÓN
# ==========================================
if menu == "🏠 Inicio":
    st.title("🏠 Panel General de Operaciones")
    st.markdown("Supervisa el estado de la colección, las existencias en stock y los resultados comerciales.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💎 Tipos de Piezas", len(st.session_state.catalogo_piezas))
    with col2:
        total_unidades = int(st.session_state.catalogo_piezas["stock"].sum())
        st.metric("📦 Unidades en Stock", f"{total_unidades} uds.")
    with col3:
        total_ventas = st.session_state.ventas_realizadas["precioventa"].sum()
        st.metric("💰 Ventas Totales", f"${total_ventas:,.0f}")
    with col4:
        prom_nota = st.session_state.ventas_realizadas["notaEva"].mean()
        st.metric("⭐ Evaluación Media", f"{prom_nota:.1f} / 5.0")
    
    st.markdown("---")
    st.subheader("🌟 Especímenes Destacados del Catálogo")
    
    cols = st.columns(3)
    for index, row in st.session_state.catalogo_piezas.head(3).iterrows():
        with cols[index % 3]:
            with st.container(border=True):
                st.markdown(f"### 💠 {row['nombrePieza']}")
                st.write(f"🏷️ **Clasificación:** {row['tipoPieza']}")
                st.write(f"🏛️ **Colección:** {row['nombreColeccion']}")
                st.write(f"📦 **Stock Disponible:** {row['stock']} uds.")
                st.write(f"💰 **Valor Est.:** ${row['valorEstimado']:,.0f}")
                st.markdown(f'<a href="{row["fuente"]}" target="_blank" class="ref-link">🔗 Ver ficha geológica oficial</a>', unsafe_allow_html=True)

elif menu == "📋 Registro de Ventas":
    st.title("📋 Historial de Registro de Ventas")
    st.markdown("Listado completo de todas las transacciones comerciales registradas en la planilla.")
    st.dataframe(st.session_state.ventas_realizadas, use_container_width=True)
    
    if not st.session_state.ventas_realizadas.empty:
        fig = px.bar(st.session_state.ventas_realizadas, x="nombrePieza", y="precioventa", color="nombreCliente", 
                     title="Comparativa de Precios de Venta por Pieza y Cliente")
        st.plotly_chart(fig, use_container_width=True)

elif menu == "💎 Catálogo":
    st.title("💎 Catálogo de Minerales, Gemas y Fósiles")
    st.markdown("Explora las piezas oficiales únicas organizadas en vitrinas virtuales con sus respectivas fuentes.")
    
    cols_per_row = 3
    piezas = st.session_state.catalogo_piezas
    
    for i in range(0, len(piezas), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(piezas):
                row = piezas.iloc[i + j]
                icono = "💎" if row["tipoPieza"] == "Gema" else ("🪨" if row["tipoPieza"] == "Mineral" else "🐚")
                with cols[j]:
                    with st.container(border=True):
                        st.markdown(f"### {icono} {row['nombrePieza']}")
                        st.write(f"🏷️ **Tipo:** {row['tipoPieza']}")
                        st.write(f"🏛️ **Colección:** {row['nombreColeccion']}")
                        st.write(f"💰 **Valor Est.:** ${row['valorEstimado']:,.0f}")
                        st.write(f"📦 **Stock:** {row['stock']} uds.")
                        st.markdown(f'<a href="{row["fuente"]}" target="_blank" class="ref-link">🔗 Ver artículo de referencia</a>', unsafe_allow_html=True)

elif menu == "📦 Inventario":
    st.title("📦 Inventario de Rocas, Minerales y Gemas")
    st.markdown("Control de especímenes en stock y cantidades disponibles.")

    df_stock = st.session_state.catalogo_piezas[["nombrePieza", "tipoPieza", "nombreColeccion", "stock"]].copy()
    df_stock.columns = ["Nombre del Espécimen", "Tipo", "Colección", "Cantidad en Stock"]

    # Métrica resumen
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Tipos de Rocas / Minerales", len(df_stock))
    with col_m2:
        st.metric("Total Unidades Físicas en Stock", int(df_stock["Cantidad en Stock"].sum()))

    st.markdown("---")
    st.subheader("📋 Listado de Stock Actual")
    st.dataframe(df_stock, use_container_width=True)

    # Gráfico simple de stock
    fig_stock = px.bar(
        df_stock, x="Nombre del Espécimen", y="Cantidad en Stock", color="Tipo",
        text="Cantidad en Stock", title="Cantidad de Stock por Roca, Mineral o Gema"
    )
    st.plotly_chart(fig_stock, use_container_width=True)

elif menu == "🛒 Registrador de Ventas":
    st.title("🛒 Registrador de Nuevas Ventas")
    with st.form("form_registrar_venta"):
        st.markdown("Complete los datos de la transacción comercial (descuenta 1 unidad del inventario automáticamente):")
        c1, c2 = st.columns(2)
        with c1:
            cliente_txt = st.text_input("Nombre del Cliente", "Museo de Historia")
            pieza_sel = st.selectbox("Seleccionar Pieza del Catálogo", st.session_state.catalogo_piezas["nombrePieza"].tolist())
        with c2:
            val_sug = float(st.session_state.catalogo_piezas[st.session_state.catalogo_piezas["nombrePieza"] == pieza_sel]["valorEstimado"].values[0])
            precio_val = st.number_input("Precio Final de Venta ($)", min_value=0.0, value=val_sug)
            expo_txt = st.text_input("Nombre de Exposición", "Mineralia 2026")
        
        nota_val = st.slider("Evaluación de la Transacción (1 al 5)", 1, 5, 5)
        
        btn_reg_venta = st.form_submit_button("Guardar Venta en el Sistema")
        if btn_reg_venta:
            idx_pieza = st.session_state.catalogo_piezas[st.session_state.catalogo_piezas["nombrePieza"] == pieza_sel].index[0]
            stock_disp = int(st.session_state.catalogo_piezas.at[idx_pieza, "stock"])
            
            if stock_disp <= 0:
                st.error(f"⚠️ No queda stock disponible de '{pieza_sel}' en el inventario.")
            else:
                id_p_sel = st.session_state.catalogo_piezas.at[idx_pieza, "idPieza"]
                nueva_vta = pd.DataFrame([{
                    "idDetalleVenta": f"DV0{len(st.session_state.ventas_realizadas)+1}",
                    "idCliente": "CL_NEW",
                    "nombreCliente": cliente_txt,
                    "idPieza": id_p_sel,
                    "nombrePieza": pieza_sel,
                    "precioventa": precio_val,
                    "nombreExposicion": expo_txt,
                    "notaEva": nota_val
                }])
                st.session_state.ventas_realizadas = pd.concat([st.session_state.ventas_realizadas, nueva_vta], ignore_index=True)
                st.session_state.catalogo_piezas.at[idx_pieza, "stock"] = stock_disp - 1
                st.success(f"✅ ¡Venta de '{pieza_sel}' registrada! Stock restante: {stock_disp - 1} uds.")

elif menu == "➕ Registrador de Minerales":
    st.title("➕ Registrador de Nuevos Minerales / Piezas")
    with st.form("form_registrar_mineral"):
        st.markdown("Ingrese los datos para dar de alta una nueva pieza o mineral en el catálogo y su stock inicial.")
        c1, c2 = st.columns(2)
        with c1:
            id_p = st.text_input("ID de Pieza (ej. PZ06)", "PZ06")
            nom_p = st.text_input("Nombre de la Pieza", "Malaquita Verde")
            tipo_p = st.selectbox("Tipo de Pieza", ["Mineral", "Gema", "Fósil"])
            stock_ini = st.number_input("Stock Inicial (unidades)", min_value=1, value=10, step=1)
        with c2:
            id_c = st.text_input("ID de Colección", "CO04")
            nom_c = st.text_input("Nombre de Colección", "Magia Nativa")
            val_e = st.number_input("Valor Estimado ($)", min_value=0.0, value=95000.0)
        
        fuente_url = st.text_input("URL de Referencia / Fuente", "https://geologyscience.com")
            
        btn_reg_min = st.form_submit_button("Agregar Pieza al Inventario")
        if btn_reg_min:
            nueva_pieza = pd.DataFrame([{
                "idPieza": id_p, "nombrePieza": nom_p, "tipoPieza": tipo_p,
                "idColeccion": id_c, "nombreColeccion": nom_c, "valorEstimado": val_e,
                "stock": stock_ini, "fuente": fuente_url
            }])
            st.session_state.catalogo_piezas = pd.concat([st.session_state.catalogo_piezas, nueva_pieza], ignore_index=True)
            st.success(f"🎉 ¡La pieza '{nom_p}' fue registrada con éxito con {stock_ini} unidades en stock!")