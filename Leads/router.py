from fastapi import APIRouter

from Leads.schema import BitrixCreate
from .bitrixapi import BitrixAPI
from .schema import BitrixUpdateRecord, BitrixUser, BitrixUpdateCompany, BitrixCreateTarrifPaid

bitrix_router = APIRouter(prefix='/BitrixAPI')


@bitrix_router.post('/lead', name="Add lead")
async def bitrix_lead(lead: BitrixUser):
    await BitrixAPI().add_lead(name=lead.name,
                               username=lead.username,
                               telegram_id=lead.telegram_id,
                               phone=lead.phone)
    return {"response": "ok"}


@bitrix_router.post('/update', name="Update lead record")
async def bitrix_update(lead: BitrixUpdateCompany):
    await BitrixAPI().lead_create_company(telegram_id = lead.telegram_id,
                                          company_link = lead.company_link,
                                          company_name = lead.company_name)
    return {"response": "ok"}


@bitrix_router.post('/create_tariff_paid', name="Create tariff paid")
async def bitrix_create_tariff_paid(lead: BitrixCreateTarrifPaid):
    await BitrixAPI().lead_create_tariff_paid(telegram_id=lead.telegram_id,
                                              tariff=lead.tariff,
                                              company_name=lead.company_name,
                                              payment_id=lead.payment_id,
                                              company_link=lead.company_link,
                                              semantic_words=lead.semantic_words,
                                              telegram_username=lead.telegram_username,
                                              )
    return {"response":'ok'}



@bitrix_router.get('/list_of_leads', name='List leads')
async def bitrix_list_of_leads():
    result = await BitrixAPI().list_of_leads()
    return result


@bitrix_router.get('/lead_by_telegram_id', name='Lead by telegram_id')
async def bitrix_lead_by_telegram_id(telegram_id: str):
    result = await BitrixAPI().lead_by_telegram_id(telegram_id=telegram_id)
    return result


@bitrix_router.post('/lead_register', name="Register lead")
async def bitrix_lead_register(telegram_id: str, phone: str):
    await BitrixAPI().lead_register(telegram_id=telegram_id,
                                    phone=phone)
    return {'response':'ok'}

    
@bitrix_router.post('/lead_diagnosis_register', name="Diagnosis register")
async def bitrix_lead_diagnosis_register(telegaram_id: str):
    await BitrixAPI().lead_diagnosis_register(telegram_id=telegaram_id)
    return {'response':'ok'}


@bitrix_router.post('/lead_investor_register', name="Investor register")
async def bitrix_lead_investor_register(telegaram_id: str):
    await BitrixAPI().lead_investor_register(telegram_id=telegaram_id)
    return {'response':'ok'}
