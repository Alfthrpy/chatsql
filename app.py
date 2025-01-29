import gradio as gr
from agents import agent, createConnection, getAllTable, Inference, set_connection

def connect(username, password, host,port, database):
    print("test")
    global conn
    conn = createConnection(username, password, host,port, database)
    set_connection(conn)
    if conn:
        tables = getAllTable(conn)  # Mengambil data setelah koneksi berhasil
        return (
            conn, 
            gr.update(value="✅ Connect Success", visible=True),  # Menampilkan toast sukses
            gr.update(value=tables, visible=True)  # Menampilkan tabel setelah connect
        )
    return None, gr.update(value="❌ Connection Failed", visible=True), gr.update(visible=False)

def yapping(message,history):
    print(history)
    global conn
    result = Inference(conn,message)
    return str(result) 


with gr.Blocks() as demo:
    state = gr.State(None)
    gr.Markdown("# Yapping to SQL")

    with gr.Tab("Chatbot"):
        gr.ChatInterface(fn=yapping, type='messages',title="Chatsql")
        gr.Markdown('Data and chat history are not being collected, so there\'s no need to worry about misuse of your information.')

    with gr.Tab("Database"):
        gr.Markdown("### Database Connection")
        gr.Markdown("Use only a cloud-hosted MySQL server (local servers are not supported).\n\nYou can use the demo server (if desired).")
        host = gr.Textbox(placeholder="http://127.0.0.1/", label="Host", value='mysql-13c1c04a-alfthr378-61ca.d.aivencloud.com')
        port = gr.Textbox(placeholder="Port", label="Port", value='16222')
        username = gr.Textbox(placeholder="Username", label="Username", value='chatsqlrek')
        password = gr.Textbox(placeholder="Password", type="password", label="Password", value='123456789')
        database = gr.Textbox(placeholder="Database", label="Database", value='sakila')

        toast = gr.Markdown(visible=False)  # Feedback setelah tombol ditekan
        btn = gr.Button("Connect")

        gr.Markdown("### Database Info")
        tables_output = gr.Textbox(visible=False)  # Awalnya disembunyikan

        btn.click(fn=connect, inputs=[username, password, host,port, database], outputs=[state, toast, tables_output])

demo.launch()
