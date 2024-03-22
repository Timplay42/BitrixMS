from BaseServiceAPI import BaseServiceAPI
from SingltonMeta import SingletonMeta
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv("BASE_API"))

class BitrixAPI(BaseServiceAPI, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__(base_api=os.getenv("BASE_API"))
    async def upload_pdf_file(self, pdf_file):  # todo тест
        try:
            import requests
            from io import BytesIO
            access_token = 'your_access_token'
            pdf_data = await pdf_file.read()
            file_obj = BytesIO(pdf_data)

            files = {'file': ('file_test.pdf', file_obj)}
            url = os.getenv("SOME_API")

            response = await self.post(url, data=files)  # todo првоерить url, которая внутри будет лежать

            return response.json()['result']['ID']
        except:
            return False

    async def lead_create_pdf(self, telegram_id: str, pdf_file):
        lead = await self.lead_by_telegram_id(telegram_id)
        pdf_id = await self.upload_pdf_file(pdf_file)

        if lead["result"]:
            url = "crm.lead.update"
            try:
                params = {
                    "id": lead["result"][0]["ID"],
                    "fields[UF_CRM_1709738723]": pdf_id  # +[data] ?
                }
                return await self.post(url, params=params)
            except Exception as error:
                print("BitrixAPI.lead_create_pdf")

    async def lead_create_tariff_paid(self, telegram_id, tariff, company_name, payment_id, company_link,semantic_words, telegram_username):
        lead = await self.lead_by_telegram_id(telegram_id)

        if lead["result"]:
            lead_url = "crm.lead.update.json"
            try:
                lead_id = lead["result"][0]["ID"]
                params = {
                    "id": lead_id,
                    "fields[UF_CRM_1710444652266]": f'Тариф: {tariff}',
                    "fields[UF_CRM_1710444679691]": 1,
                    "fields[UF_CRM_1710444716134]": f'{payment_id}',
                    "fields[UF_CRM_1710444795955]": f'{company_link}',
                    "fields[UF_CRM_1710498029057]": f'{semantic_words}',
                    "fields[STATUS_ID]": "UC_CCD607",
                }
                await self.post(lead_url, params=params)
                deal_url = "crm.deal.add"
                params = {
                    "fields[LEAD_ID]": lead_id,
                    "fields[UF_CRM_1710498099224]": semantic_words,
                    "fields[UF_CRM_1710498115135]": company_link,
                    "fields[UF_CRM_1710770165458]": f"t.me/{telegram_username}",
                    "fields[UF_CRM_1710499866964]": tariff,
                    "fields[UF_CRM_1710770299777]": str(telegram_id),
                    "fields[STATUS_ID]": "C10:UC_4ZW2YB",
                    "fields[TITLE]": f"{company_name} - {tariff}",
                }
                print(params)
                return await self.post(deal_url, params=params)
            except Exception as error:
                print("BitrixAPI.lead_create_tariff_paid", error)

    async def add_lead(self, name: str, username: str, telegram_id: str, phone: str, where: str = "Bot"):
        url = "crm.lead.add.json"
        params = {
            "fields[TITLE]": f"Заявка с {where}, {name}",
            "fields[NAME]": name,
            "fields[UF_CRM_1703859262115]": username,
            "fields[UF_CRM_1703859243479]": telegram_id,
            "fields[UF_CRM_1697212301233]": 0,
            "fields[UF_CRM_1697466198798]": where,
            "fields[PHONE][0][VALUE]": phone,
            "fields[PHONE][0][VALUE_TYPE]": "WORK"
        }
        try:
            return await self.post(url, params=params)
        except Exception as error:
            print("BitrixAPI.add_lead", error)



    async def lead_create_record(self, telegram_id, phone: str):
        lead = await self.lead_by_telegram_id(telegram_id)
        if lead["result"]:
            url = "crm.lead.update.json"
            try:
                params = {
                    "id": lead["result"][0]["ID"],
                    "fields[PHONE][0][VALUE]": phone,
                }
                return await self.post(url, params=params)
            except Exception as error:
                print("BitrixAPI.lead_record", error)

    async def list_of_leads(self):
        url = "crm.lead.list.json"
        params = {"select[]": "EMAIL"}
        try:
            return await self.get(url, params=params)
        except Exception as error:
            print("BitrixAPI.list_of_leads", error)

    async def lead_by_telegram_id(self, telegram_id):
        url = "crm.lead.list.json"
        params = {"select[]": "NAME", "filter[UF_CRM_1703859243479]": str(telegram_id)}
        try:
            return await self.get(url, params=params)
        except Exception as error:
            print("BitrixAPI.lead_by_email", error)

    async def lead_create_company(self, telegram_id, company_link: str = None, company_name: str = None):
        lead = await self.lead_by_telegram_id(telegram_id)
        print(lead)
        if lead["result"]:
            url = "crm.lead.update.json"
            try:
                params = {
                    "id": lead["result"][0]["ID"],
                    "fields[UF_CRM_1703859538225]": company_link,
                    "fields[UF_CRM_1703859526101]": company_name,
                }
                return await self.post(url, params=params)
            except Exception as error:
                print("BitrixAPI.lead_create_company", error)

    async def lead_register(self, telegram_id, phone: str):
        lead = await self.lead_by_telegram_id(telegram_id)
        if lead["result"]:
            url = "crm.lead.update.json"
            try:
                params = {
                    "id": lead["result"][0]["ID"],
                    "fields[PHONE][0][VALUE]": phone,
                    "fields[PHONE][0][VALUE_TYPE]": "WORK"
                }
                return await self.post(url, params=params)
            except Exception as error:
                print("BitrixAPI.lead_register", error)

    async def lead_diagnosis_register(self, telegram_id):
        lead = await self.lead_by_telegram_id(telegram_id)
        if lead["result"]:
            url = "crm.lead.update.json"
            try:
                params = {
                    "id": lead["result"][0]["ID"],
                    "fields[STATUS_ID]": "UC_RBLRRG",
                }
                return await self.post(url, params=params)
            except Exception as error:
                print("BitrixAPI.lead_diagnosis_register", error)

    async def lead_investor_register(self, telegram_id):
        lead = await self.lead_by_telegram_id(telegram_id)
        if lead["result"]:
            url = "crm.lead.update.json"
            try:
                params = {
                    "id": lead["result"][0]["ID"],
                    "fields[STATUS_ID]": "UC_JOQT9R",
                }
                return await self.post(url, params=params)
            except Exception as error:
                print("BitrixAPI.lead_paid", error)

if __name__ == '__main__':
    import asyncio


    async def main():
        result = await BitrixAPI().add_lead("test", "+73984173191", "mail@mail.ru")
        #result = await BitrixAPI().lead_diagnosis_register("577703143")


    asyncio.run(main())
