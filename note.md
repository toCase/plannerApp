requirements.txt

pip freeze > requirements.txt

python manage.py makemigrations
python manage.py migrate

----Colors----

    --clr-bg:#fafbfe;

    --clr-menu-bg: #0e2238;
    --clr-menu-txt: #fff;
    --clr-menu-bg-act: rgba(255, 255, 255, .075);
    --clr-menu-bg-hov: rgba(255, 255, 255, .015);
    --clr-menu-sec:#3B7DDD;

    --clr-txt-dark: #000;
    --clr-txt-light:  #F9ECD6;

    --clr-cal-today: rgb(228, 176, 85);
    --clr-cal-select: #16a45466;
    --clr-cal-hover: #9f1f34;

    --clr-form-bg: rgb(217, 217, 217);

    --clr-meet: #EAEAEA;
    --clr-m-value: #0e2238;
    --clr-m-report: #2A6416;
    --clr-m-review: #9C6107;

----Правила----

*Notes
    FRM - firm
    SLN - saloon
    SPE_SEARCH, 
    SPE_PAGE,

*Создание фирмы

    - нужно создать САЛОН с меткой MAIN

*Салоны

    ** Удаление 

        - при удаление САЛОНа с меткой МАИН -- метку переставить на другой салон
        - если остался один салон - его удалять нельзя 

*Шаблоны рабочих графиков

    ** Удаление
        -- выбираются актуальные шаблоны (те у которых даты в календаре gte от сегодня)
        -- удалить можно только неактуальные
        

----***-----


----TODO----

Календарный график

    - при добавлении специалиста сделать множественный выбор дат
        -- в форме выбор между одной (текущей датой) и множественным выбором (radio buttons)
        -- при множественном выборе
            --- поменять календарь
            --- собрать выбранные дни в список
            --- сохранение по списку дат
    - выход на страницу загальний розклад
        - таблица за месяц по дням, кто работает, в какое время


--- Состояние встреч ---

- регистрация 
    - админ - PRE
    - bot   - BOT
    - api   - API

- выполнена - DONE  
- перенос   - PREP  
- отмена    - FAIL

- оплата - PAID

План доволі простий
Я буду робити програму на Python, тож ви отримаєте такий собі app.exe. 
Інтерфейс дуже простий, будуть деяки налаштування, кнопка Старт та місце для виводу звіту про завантаження та помилок.

Що від вас буде треба.
1. Це API ключ для РРО Checkbox
2. 
    

{
    'success': True, 
    'data': [
        {
            'LightReturnNumber': '', 
            'CounterpartyRecipientDescription': '', 
            'DocumentWeight': 0.5, 
            'ServiceType': 'WarehouseWarehouse', 
            'UndeliveryReasons': '', 
            'RecipientFullName': '', 
            'FactualWeight': '0.50', 
            'MarketplacePartnerToken': '', 
            'CounterpartySenderDescription': '', 
            'InternationalDeliveryType': '', 
            'CargoType': 'Documents', 
            'PayerType': 'Recipient', 
            'SeatsAmount': '1', 
            'ScheduledDeliveryDate': '04-04-2024 13:23:50', 
            'DocumentCost': '55.01', 
            'CardMaskedNumber': '', 
            'OwnerDocumentType': '', 
            'ExpressWaybillPaymentStatus': '', 
            'ExpressWaybillAmountToPay': '', 
            'AfterpaymentOnGoodsCost': '', 
            'SumBeforeCheckWeight': 0, 
            'CheckWeight': 0, 
            'PaymentMethod': 'NonCash', 
            'AdjustedDate': '', 
            'Number': '59001129284417', 
            'TrackingUpdateDate': '2024-04-04 13:24:11', 
            'CalculatedWeight': '', 
            'WarehouseRecipient': 'Відділення №1: вул. Корсунська, 9', 
            'WarehouseSender': 'Відділення №4: вул. Євгена Чикаленка, 86', 
            'DateCreated': '03-04-2024 17:33:10', 
            'DateScan': '13:24 04.04.2024', 
            'DateReturnCargo': '', 
            'DateMoving': '', 
            'DateFirstDayStorage': '2024-04-12', 
            'DatePayedKeeping': '2024-04-12 13:23:50', 
            'RecipientAddress': '', 
            'RecipientDateTime': '', 
            'RefCityRecipient': 'f706230a-4078-11de-b509-001d92f78698', 
            'RefCitySender': 'db5c88d0-391c-11dd-90d9-001a92567626', 
            'RefSettlementRecipient': 'e714d49f-4b33-11e4-ab6d-005056801329', 
            'RefSettlementSender': 'e71c2a15-4b33-11e4-ab6d-005056801329', 
            'SenderAddress': '', 
            'ClientBarcode': '', 
            'CitySender': 'Одеса', 
            'CityRecipient': 'Богуслав (Київська обл.)', 
            'CargoDescriptionString': '', 
            'AnnouncedPrice': '', 
            'AdditionalInformationEW': '', 
            'ActualDeliveryDate': '2024-04-04 13:23:50', 
            'StatusCode': '7', 
            'PostomatV3CellReservationNumber': False, 'AmountToPay': '', 'AmountPaid': '', 'RefEW': '2f56d734-f1c7-11ee-a361-48df37b92096', 'VolumeWeight': '0.01', 'CheckWeightMethod': '', 'OwnerDocumentNumber': '', 'LastCreatedOnTheBasisNumber': '', 'LastCreatedOnTheBasisDateTime': '', 'LastTransactionDateTimeGM': '', 'PaymentStatus': '', 'PaymentStatusDate': '', 'LastAmountTransferGM': '', 'LastAmountReceivedCommissionGM': 0, 'LastCreatedOnTheBasisPayerType': '', 'DeliveryTimeframe': '', 'LastTransactionStatusGM': '', 'Status': 'Прибув у відділення', 'CreatedOnTheBasis': '', 'Redelivery': 0, 'RedeliveryNum': '', 'RedeliverySum': '', 'RedeliveryPayer': '', 'UndeliveryReasonsDate': '', 'UndeliveryReasonsSubtypeDescription': '', 'RecipientWarehouseTypeRef': '9a68df70-0267-42a8-bb5c-37f427e36ee4', 'WarehouseRecipientInternetAddressRef': 'f13871cc-96ca-11e6-a4c1-005056887b8d', 'WarehouseRecipientNumber': 1, 'WarehouseRecipientRef': 'f13871cd-96ca-11e6-a4c1-005056887b8d', 'CategoryOfWarehouse': 'Branch', 'WarehouseRecipientAddress': 'Богуслав (Київська обл.), Корсунська, 9', 'WarehouseSenderInternetAddressRef': '1ec09d63-e1c2-11e3-8c4a-0050568002cf', 'WarehouseSenderAddress': 'Одеса, Євгена Чикаленка, 86', 'CounterpartyType': 'Organization', 'CounterpartySenderType': 'PrivatePerson', 'AviaDelivery': 0, 'BarcodeRedBox': '', 'CargoReturnRefusal': False, 'DaysStorageCargo': '', 'Packaging': [], 'PartialReturnGoods': [], 'SecurePayment': False, 'StorageAmount': '', 'StoragePrice': '', 'PossibilityCreateRedirecting': True, 'PossibilityCreateReturn': True, 'PossibilityCreateRefusal': True, 'PossibilityChangeEW': True, 'PossibilityChangeCash2Card': False, 'PossibilityChangeDeliveryIntervals': False, 'PossibilityTermExtension': True, 'PossibilityTrusteeRecipient': False, 'TrusteeRecipientPhone': '', 'PossibilityLightReturn': False, 'PossibilityCreateClaim': False, 'RedeliveryPaymentCardRef': '', 'RedeliveryPaymentCardDescription': '', 'FreeShipping': '', 'InternetDocumentDescription': '', 'LastCreatedOnTheBasisDocumentType': '', 'LoyaltyCardRecipient': '', 'LoyaltyCardSender': '', 'PhoneRecipient': '', 'PhoneSender': '', 'RecipientFullNameEW': '', 'RedeliveryServiceCost': '', 'SenderFullNameEW': ''}], 'errors': [], 'warnings': [{'ID_59001129284417': 'Please enter a valid phone number from the express invoice to show full information'}], 'info': [], 'messageCodes': [], 'errorCodes': [], 'warningCodes': [], 'infoCodes': []}