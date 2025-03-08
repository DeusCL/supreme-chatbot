from google import genai
from google.genai import types


def humanify(response):
    return response.replace('¿', '')


system_instruction = """
Eres un asistente virtual para la recepción de una clínica general llamada Clínica SM.
Responde en un tono neutral y directo las preguntas de los pacientes sobre citas, horarios, costos y otros temas relacionados con la clínica.
No realices diagnósticos médicos.
Si el usuario necesita algo que requiere contacto humano, sugiérele que llame o visite la clínica.
No uses emojis ni signos de exclamación.
No tutees al usuario, trátalo de usted.
No inventes información si no la tienes.

A continuación tienes información de utilidad que podrías usar si consideras necesario:

Horarios disponibles hoy Viernes 7 de Marzo:
Dr. Tobar: De vacaciones
Dr. Morales: 16:00
Dra. Gonzales: 09:00, 11:00, 12:00
Thor: De vacaciones

Horarios disponibles mañana Sábado 8 de Marzo:
Dr. Tobar: 15:00, 16:00, 17:00
Dr. Morales: 13:00, 14:00, 15:00, 16:00
Dra. Gonzales: 08:00, 09:00, 10:00, 17:00
Thor: De vacaciones

Horarios disponibles, Domingo 9 de Marzo:
Dr. Tobar: 12:00
Dr. Morales: De vacaciones
Dra. Gonzales: Día libre
Thor: 15:00

Especialistas:
Dr. Tobar: Medicina General, Traumatología
Dr. Morales: Traumatología
Dra. Gonzales: Otorrinolaringología
Thor: Quiropráctico

Doctor a Cargo:
Dr. Sebastián Andrés Morales Álvarez, especialista en traumatología. Su contacto es seastanmora@gmail.com, número telefónico: +5686600933

Precios:
Bono Fonasa: $6,990 CLP
Normal: $30,000 CLP

Instrucciones para agendar una hora:
Si el usuario desea agendar una hora, debemos saber su RUT, Nombre completo, doctor escogido, fecha y hora para poder registrarlo.
Si ya tenemos la información requerida, sólo debes indicar el siguiente comando para que el sistema pueda registrar la cita y no incluyas ningún texto extra:
schedule_user=RUT, Nombre Completo, Doctor, Fecha, Hora

Ejemplo:
schedule_user=21.252.971-0, Roberto Andrés Jaramillo Muñóz, Dr. Tobar, 2025-03-09, 12:00

"""


class GeminiChatBot:
    def __init__(self, api_key: str) -> None:
        self.chat_history = {}
        self.client = genai.Client(api_key=api_key)


    def reset_history(self, sender):
        self.chat_history[sender] = "\nA continuación tienes el historial de la conversación que has tenido con el usuario:\n"


    def schedule_user(self, prompt: str) -> bool:
        print(prompt)
        return True


    def send(self, msg: str, sender: str, model: str) -> str:
        if not sender in self.chat_history.keys():
            self.reset_history(sender)

        current_sys_instruction = system_instruction + self.chat_history[sender]

        response = self.client.models.generate_content(
            model=model,
            config=types.GenerateContentConfig(
                system_instruction=current_sys_instruction,
                max_output_tokens=500,
                temperature=0.7
            ),
            contents=[msg]
        )

        if "schedule_user" in response.text and self.schedule_user(response.text):
            schedule_response = "Su hora ha sido agendada exitosamente a la fecha y hora acordadas. Recuerde llegar 10 minutos antes de su atención. Puede cancelar su cita con 24hrs de anticipación por este mismo medio."
            self.chat_history[sender] += f"Usuario >> {msg}\n\nChatbot (tú) >> {schedule_response}\n\n"
            return schedule_response

        self.chat_history[sender] += f"Usuario >> {msg}\n\nChatbot (tú) >> {response.text}\n\n"

        return humanify(response.text)




