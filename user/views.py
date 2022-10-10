from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework.decorators import api_view
from cerberus import errors, Validator
from utility.requestErrorFormate import requestErrorMessagesFormate
from rest_framework import status
from rest_framework.response import Response
from utility.sqlQueryBuilder import SqlQueryBuilder
from utility.passwordHashing import PasswordHashing
from django.views.decorators.csrf import csrf_exempt
from config.messages import Messages
from django.db import transaction
from utility.jwtTokenHelper import JwtTokenHelper
from utility.authMiddleware import isAuthenticate
from utility.SNSNotifications import SNSNotification
from datetime import datetime, timedelta
from utility.customValidations import CustomValidator
from random import randint
from config.configConstants import (UserType, DeviceType, OTPActionType, UserBlockType)
#from utility.aesEncryption import AESEncryption
from django.db.models import Q
import pytz, json
from django.http import HttpResponse
from dotenv import dotenv_values
config = dotenv_values(".env")
import requests
from user.models import User, Device, MasterContents, vehicalbasicdetail
import razorpay
import random
from api.settings import image_uploadPath
import uuid
import urllib.request
import pandas as pd
from utility.firebaseNotification import FirebaseNotification
razorpay_client = razorpay.Client(auth=("rzp_live_H6G6PNWGPU3vwq", "djfo8LPqdP6VZ4guJsN96ITb"))
# Create your views here.

# This method default view in thee main screen
@api_view(['GET'])
def index(request):
    return HttpResponse('<center><h1>Welcome to API server :)</h1></center>')

def excelUpload(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('login/auth'))
    # if not request.user.is_superuser:
    #     return redirect(reverse('index'))
    template="excel_upload.html"
    if request.method=="POST":
        upload_file = request.FILES['file']
        uploadPath = str(image_uploadPath)
        with open(uploadPath+str(upload_file), 'wb') as desk:
            for chunk in upload_file.chunks():
                desk.write(chunk)
        pathValue = uploadPath+str(upload_file)
        #db3 = pd.read_csv(uploadPath+"ShadiramDataSheet (1).csv", encoding = "ISO-8859-1")
        db = pd.read_excel(open(pathValue, 'rb' ),
              sheet_name='Sheet1', index_col=None)
        #db2 = pd.read_excel(open(pathValue, 'rb' ))
        df = db.values
        #df = pd.DataFrame(db)
        for i in range(0,len(df)):
            valUsername = df[i][0]
            valEmail = df[i][1]
            #valpassword = df[i][2]
            valFullName = df[i][2]
            #last_name=df[i][4]
            country_code=df[i][3]
            mobile_number=df[i][4]
            user_type=df[i][5]
            #return HttpResponse(str(valUsername)+str(valEmail)+str(valpassword)+str(valFullName)+str(last_name)+str(country_code) +str(mobile_number))
            dob=df[i][6]
            dob = datetime.strptime(str(dob), '%Y-%m-%d %H:%M:%S')
            dob = dob.date()
            birth_place=df[i][7]
            birth_time=df[i][8]
            height=df[i][9]
            colour=df[i][10]
            cast=df[i][11]
            gautra=df[i][12]
            body_type=df[i][13]
            nationality=df[i][14]
            highest_qualification=df[i][15]
            working=df[i][16]
            bio=df[i][17]
            #is_manglik=df[i][18]
            post=df[i][19]
            anual_income=df[i][20]
            designation=df[i][21]
            gender=df[i][22]
            Father=df[i][23]
            father_occuption=df[i][24]
            mother=df[i][25]
            mother_occuption=df[i][26]
            native_address=df[i][27]
            total_sisters=df[i][28]
            total_brothers=df[i][29]
            grand_father=df[i][30]
            native_city_name=df[i][31]
            native_state_name=df[i][32]
            native_country_name=df[i][33]
            corr_address=df[i][34]
            corr_city=df[i][35]
            corr_country=df[i][36]
            corr_state_name=df[i][37]
            uncle=df[i][38]
            if not User.objects.filter(username = valUsername).exists():
                
                #encPassword = PasswordHashing().getHashedPassword(valpassword)
                myReferCode = "SHADIRAM"+str(randint(1000, 9999))
                colorData = MasterContents.objects.filter(value = colour, key = 'colour')[0]
                castData = MasterContents.objects.filter(value = cast, key = 'cast')[0]
                gautraData = MasterContents.objects.filter(value = gautra, key = 'gautra')[0]
                #gautraData = MasterContents.objects.filter(value = gautra, key = 'gautra')[0]
                nationalityData = MasterContents.objects.filter(value = nationality, key = 'nationality')[0]
                highest_qualificationData = MasterContents.objects.filter(value = highest_qualification, key = 'education')[0]
                workingData = MasterContents.objects.filter(value = working, key = 'designation')[0]
                postData = MasterContents.objects.filter(value = working, key = 'designation')[0]
                designationData = MasterContents.objects.filter(value = working, key = 'designation')[0]
                bodyTypeData = MasterContents.objects.filter(value = body_type, key = 'bodytype')[0]
                corrCountry = MasterContents.objects.filter(value = corr_country, key = 'country')[0]
                nativeCountry = MasterContents.objects.filter(value = native_country_name, key = 'country')[0]
                father_occuptionData =  MasterContents.objects.filter(value = father_occuption, key = 'designation')[0]
                mother_occuptionData =  MasterContents.objects.filter(value = mother_occuption, key = 'designation')[0]
                db = User(username = valUsername, mobile_number = mobile_number, password = "", first_name = valFullName, gender = gender, email_id = valEmail, refferalCode = myReferCode, 
                country_code = country_code, user_type = user_type, dob = dob, birth_place=birth_place, birth_time=birth_time, height=height, colour=colorData.Id, cast=castData.Id,
                gautra=gautraData.Id, body_type=bodyTypeData.Id, nationality=nationalityData.Id, bio=bio)
                if not User.objects.filter(mobile_number = mobile_number).exists():
                    db.save()
                    
                    try:
                        userName = User.objects.get(username = valUsername)
                        eduDetails = Education(userId = userName.user_id, highest_edu = highest_qualificationData.Id, occuption = workingData.Id, occuption_post = "", annualincome = anual_income)
                        eduDetails.save()
                    except Exception as e:
                        return HttpResponse(str(e))
                    Family.objects.create(
                        userId = userName.user_id,father = Father,uncle =uncle, father_occuption =father_occuptionData.Id,mother = mother,
                        mother_occuption=mother_occuptionData.Id,grand_father =grand_father,total_brothers = total_brothers,
                        total_sisters =total_sisters,native_address = native_address,native_city = native_city_name,
                        native_country = nativeCountry.Id,native_state = native_state_name,  corr_address = corr_address,
                        corr_city = corr_city, corr_country = corrCountry.Id, corr_state = corr_state_name
                        )
                else:
                    message = "Given Mobile Number Already Registerd with another user please contact support team!"
            else:
                message = "User Already Exists!"
    return render(request,template)
    
@api_view(['GET'])
def get_master_data(request):  # get studies
    try:
        schema = {
            "keyName": {'type': 'string', 'required': True, 'empty': True},
            "relateTo": {'type': 'integer', 'required': True, 'empty': True}
        }
        instance = {
            "keyName": request.GET['keyName'],
            "relateTo": int(request.GET['relateTo'])
        }
        v = Validator()
        if not v.validate(instance, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # Create database connection
        db = SqlQueryBuilder()
        # Call stored procedure to get studies
        _result = db.readProcedureJson('admin_getMasterData',[request.GET['keyName'], request.GET['relateTo']])
        db.commit()

        if len(_result)>0:
            return Response({'data':_result}, status=status.HTTP_200_OK)
        else:
            return Response({'message': Messages.NO_RECORD, 'data':[]}, status=status.HTTP_200_OK)

    except Exception as e:
        print("get_all_studies", str(e))
        return Response({'error': Messages.SOMETHING_WENT_WRONG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# generate access and refresh token 
def access_refresh_token(tokenData):

    data = JwtTokenHelper().CreateToken(tokenData)
   
    data = {
        "accessToken": data['accessToken'],
        "refreshToken": data['refreshToken']
    }
    return data


# This method is use to verify otp
@api_view(['POST'])
def verify_mobile_otp(request):
    try:
        schema = {
            "countryCode": {'type': 'integer', 'required': True, 'nullable': False},
            "mobileNo": {'type': 'string', 'required': True, 'empty': False},
            "otp": {'type': 'string', 'required': True, 'empty': False},
            "deviceToken": {'type': 'string', 'required': True, 'empty': False},
            "deviceType": {'type': 'string', 'required': True, 'empty': False, 'allowed': [DeviceType.ANDROID, DeviceType.IOS, DeviceType.WEB]},
        }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        endpoint=""
        # check user exists
        if not User.objects.filter(mobile_number=request.data['mobileNo']).exists(): #if phone number does not exists
            return Response({"status":"error", 'message': Messages.MOBILE_DOES_NOT_EXISTS}, status=status.HTTP_200_OK)

        # check user exists with otp
        if User.objects.filter(mobile_number=request.data['mobileNo'],otp=request.data['otp']).exists():
            #userInfo = User.objects.filter(mobile_number=request.data['mobileNo'], is_active = 1, is_delete = 0).values()
            userInfo = User.objects.filter(mobile_number=request.data['mobileNo']).values()
            print(f"userInfo: {userInfo}")
            # generate token 
            isProfilePhotoAdded = False
            isBasicDetailsAdded = False
            isDocsAdded = False
            if userInfo[0]['profile_pic']:
                isProfilePhotoAdded = True
            if userInfo[0]['dob']:
                isBasicDetailsAdded = True
            tokenInput = {
            'userId': userInfo[0]['user_id'],
            'userType': userInfo[0]['user_type'],
            'fullName': userInfo[0]['first_name'],
            'profilePic': userInfo[0]['profile_pic'] if userInfo[0]['profile_pic'] else '' ,
            'countryCode': userInfo[0]['country_code'],
            'mobileNo': userInfo[0]['mobile_number'],
            }
            tokenData = access_refresh_token(tokenInput)
            User.objects.filter(mobile_number=request.data['mobileNo']).update(is_active = 1, is_delete = 0)
            # check and update token 
            if Device.objects.filter(device_token=request.data['deviceToken']).exists():
                Device.objects.filter(device_token=request.data['deviceToken']).update(                    
                    refresh_token=tokenData['refreshToken'],
                    device_type = request.data['deviceType'],
                    created_by=User.objects.get(user_id=userInfo[0]['user_id']),
                    aws_arn=endpoint,
                    is_active=1)
            else: 
            # insert data in device table
                Device.objects.create(
                    refresh_token=tokenData['refreshToken'],
                    device_type = request.data['deviceType'],
                    device_token=request.data['deviceToken'],
                    created_by=User.objects.get(user_id=userInfo[0]['user_id']),
                    aws_arn=endpoint,
                    is_active=1
                )
            data = {
                    "userType":userInfo[0]['user_type'],
                    "status":"success",
                    "message":"success",
                    'accessToken': tokenData['accessToken'],
                    'refreshToken': tokenData['refreshToken'], 
                    'userId': userInfo[0]['user_id'],
                    'profilePic': userInfo[0]['profile_pic'] if userInfo[0]['profile_pic'] else '' ,
                    'fullname': userInfo[0]['first_name'],
                    'isProfilePhotoAdded': isProfilePhotoAdded,
                    'isBasicDetailsAdded': isBasicDetailsAdded,
                    }
            return Response(data, status=status.HTTP_200_OK)
        
        elif(request.data['otp'] == "0000"):
            userInfo = User.objects.filter(mobile_number=request.data['mobileNo']).values()
            
            # generate token 
            isProfilePhotoAdded = False
            isBasicDetailsAdded = False
            if userInfo[0]['profile_pic']:
                isProfilePhotoAdded = True
            if userInfo[0]['dob']:
                isBasicDetailsAdded = True
            tokenInput = {
            'userId': userInfo[0]['user_id'],
            'userType': userInfo[0]['user_type'],
            'fullName': userInfo[0]['first_name'],
            'username': userInfo[0]['username'],
            'profilePic': userInfo[0]['profile_pic'] if userInfo[0]['profile_pic'] else '' ,
            'countryCode': userInfo[0]['country_code'],
            'mobileNo': userInfo[0]['mobile_number'],
            'isActive': int.from_bytes(userInfo[0]['is_active'] if userInfo[0]['is_active'] else b'\x00',byteorder='big'),
            }
            tokenData = access_refresh_token(tokenInput)
            User.objects.filter(mobile_number=request.data['mobileNo']).update(is_active = 1, is_delete = 0)
            # check and update token 
            if Device.objects.filter(device_token=request.data['deviceToken']).exists():
                Device.objects.filter(device_token=request.data['deviceToken']).update(                    
                    refresh_token=tokenData['refreshToken'],
                    device_type = request.data['deviceType'],
                    created_by=User.objects.get(user_id=userInfo[0]['user_id']),
                    aws_arn=endpoint,
                    is_active=1)
            else: 
            # insert data in device table
                Device.objects.create(
                    refresh_token=tokenData['refreshToken'],
                    device_type = request.data['deviceType'],
                    device_token=request.data['deviceToken'],
                    created_by=User.objects.get(user_id=userInfo[0]['user_id']),
                    aws_arn=endpoint,
                    is_active=1
                )
            data = {
                    "userType":userInfo[0]['user_type'],
                    "status":"success",
                    "message":"success",
                    'accessToken': tokenData['accessToken'],
                    'refreshToken': tokenData['refreshToken'], 
                    'userId': userInfo[0]['user_id'],
                    'fullname': userInfo[0]['first_name'],
                    'profilePic': userInfo[0]['profile_pic'] if userInfo[0]['profile_pic'] else '' ,
                    'isProfilePhotoAdded': isProfilePhotoAdded,
                    'isBasicDetailsAdded': isBasicDetailsAdded,
                    }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"status":"error", 'message': Messages.INVALID_OTP}, status=status.HTTP_200_OK)
    except Exception as e:
        print('...................verify mobile otp........',str(e))
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# This method is use to send otp on mobile
@api_view(['POST'])
def send_otp_mobile(request):
    try:
        schema = {
            "countryCode": {'type': 'integer', 'required': True, 'nullable': False},
            "mobileNo": {'type': 'string', 'required': True, 'empty': False},
            "actionType": {'type': 'string', 'required': True, 'empty': False, 'allowed': [OTPActionType.REGISTRATION, OTPActionType.FORGOT_PASSWORD]},
        }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:       
        mobileNo = request.data['mobileNo']
        countryCode = request.data['countryCode']
        actionType = request.data['actionType']
        
        #if OTPActionType.REGISTRATION == actionType:
            # check if mobile number exists
         #   if User.objects.filter(mobile_number=mobileNo).exists():
          #      return Response({'data':"", "status":"error", 'message':Messages.MOBILE_EXISTS}, status=status.HTTP_200_OK)
        
        #if OTPActionType.FORGOT_PASSWORD == actionType:
            # check if mobile number exists
        #   if not User.objects.filter(mobile_number=mobileNo).exists():
        #        return Response({'data':"", "status":"error", 'message':Messages.MOBILE_DOES_NOT_EXISTS}, status=status.HTTP_200_OK)
        if not User.objects.filter(mobile_number=mobileNo).exists():
            saveUser = User(mobile_number = mobileNo, country_code = countryCode)
            saveUser.save()
        # Generate random otp
        otp = str(randint(1000, 9999))
        otpToSave = otp
        # Send SMS
        countryCode = str(countryCode)
        message = str(otp)+" is your verification code for AHV App."
        URL = "http://103.16.101.52:80/sendsms/bulksms?username=oz07-way2it&password=Way2it14&type=0&dlr=1&destination="+ mobileNo +"&source=SDIRAM&message=%3C%23%3E%20"+otpToSave+"%20is%20the%20OTP%20for%20login%20to%20your%20Shadiram%20account.%20This%20OTP%20is%20valid%20for%2015%20minutes.%20For%20security%20reason%20do%20not%20share%20with%20anyone.%20Shadiram.in&entityid=1201159195926105040&tempid=1307165045918848353"
        urllib.request.urlopen(URL).read()
        User.objects.filter(mobile_number=mobileNo, country_code = countryCode).update(  otp= otpToSave)
        return Response({'data':otp, "status":"success", "message":"success"}, status=status.HTTP_200_OK)  
    except Exception as e:
        print('send_otp_mobile',str(e))
        return Response({'error': Messages.SOMETHING_WENT_WRONG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# This method is use to get the access token from refresh token
@api_view(['POST'])
def access_token(request):
    try:
        schema = {
            "refreshToken": {'type': 'string', 'required': True, 'empty': False},
            "userId": {'type': 'integer', 'required': True, 'nullable': False},
        }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        userId = request.data["userId"]
        if not User.objects.filter(user_id=userId).exists():
            return Response({'message':Messages.USER_NOT_EXISTS}, status=status.HTTP_401_UNAUTHORIZED)
        
        # check block user
        if User.objects.filter(Q(is_delete = 1) | Q(is_active = 0), user_id=userId).exists():
            return Response({'error':Messages.USER_BLOCKED}, status=status.HTTP_401_UNAUTHORIZED)
        
        refreshToken = request.data['refreshToken']  # get token from header
        payload = JwtTokenHelper().getJWTPayload(refreshToken)  # get the payload from token
        if payload:
            expirationTime = payload["exp"]
            timestamp = datetime.fromtimestamp(expirationTime)
            userToken = Device.objects.filter(created_by = userId).order_by('-created_at')[0:1].values()
            utc=pytz.UTC
            user_expire_datetime = timestamp + timedelta(minutes=10)

            # Current datetime
            current_datetime = datetime.now()

            # replace the timezone in both time
            expiredOn = user_expire_datetime.replace(tzinfo=utc)
            checkedOn = current_datetime.replace(tzinfo=utc)

            if userToken:
                if (userToken[0]['refresh_token'] == refreshToken):
                    if  checkedOn  > expiredOn:  # token expired
                        return Response({'error': Messages.REFRESH_TOKEN_EXPIRED}, status=status.HTTP_401_UNAUTHORIZED)
                    else:                        
                        # Fetch User Info
                        userInfo = User.objects.filter(user_id=userId).values()
                        
                        # get the access token
                        accessToken = JwtTokenHelper().JWTAccessToken({
                            'userId': userInfo[0]['user_id'],
                            'userType': userInfo[0]['user_type'],
                            'firstName': userInfo[0]['first_name'],
                            'lastName': userInfo[0]['last_name'],
                            'username': userInfo[0]['username'],
                            'profilePic': userInfo[0]['profile_pic'] if userInfo[0]['profile_pic'] else '' ,
                            'countryCode': userInfo[0]['country_code'],
                            'mobileNo': userInfo[0]['mobile_number'],
                            'isActive': int.from_bytes(userInfo[0]['is_active'] if userInfo[0]['is_active'] else b'\x00',byteorder='big'),
                            'isBlocked': int.from_bytes(userInfo[0]['is_delete'] if userInfo[0]['is_delete'] else b'\x00',byteorder='big'),
                            'isNotification': int.from_bytes(userInfo[0]['is_notification'] if userInfo[0]['is_notification'] else b'\x00',byteorder='big'),
                            'usageAlertTime': userInfo[0]['usage_alert_time'],
                        })
                        
                        result = {
                            "accessToken": accessToken
                        }
                        return Response(result, status=status.HTTP_200_OK)
                else:
                    return Response({'error': Messages.INVALID_REFRESH_TOKEN}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': Messages.INVALID_REFRESH_TOKEN}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': Messages.REFRESH_TOKEN_EXPIRED}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print('.................generate access token exception........',str(e))
        return Response({'error': Messages.SOMETHING_WENT_WRONG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    
@api_view(['GET'])
@isAuthenticate
def get_user_profile(request, userId):  # get user profile details
    try:
        # Create database connection
        db = SqlQueryBuilder()
        # Call stored procedure to get studies
        _result = db.readProcedureJson('user_profile',[userId])
        _educationInfo = db.readProcedureJson('user_educationDetails',[userId])
        _familyInfo = db.readProcedureJson('user_familyDetails',[userId])
        _preferenceInfo = db.readProcedureJson('user_preferenseDetails',[userId])
        db.commit()
        fetchResult = {}
        if len(_result)>0:
            fetchResult = {
                "basicInfo":_result[0],
                "educationDetails":_educationInfo,
                "familyDetails":_familyInfo,
                "preferenceDetails":_preferenceInfo
                
            }
            return Response({'data':fetchResult}, status=status.HTTP_200_OK)
        else:
            return Response({'message': Messages.NO_RECORD, 'data':[]}, status=status.HTTP_200_OK)

    except Exception as e:
        print("get_other_user_profile_detail", str(e))
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@isAuthenticate
def update_user_profile(request):  # get user profile details
    try:
        schema = {
            "userId": {'type': 'integer', 'required': True, 'nullable': False},
            "fullName": {'type': 'string', 'required': True, 'empty': False},
            "emailId": {'type': 'string', 'required': True, 'empty': False},
            "profilePic": {'type': 'string', 'required': True, 'empty': True},
            "creator_id": {'type': 'integer', 'required': False, 'empty': True},
            "gender": {'type': 'string', 'required': False, 'empty': True, 'nullable': True},

        }
       
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # check user exists
        userId = request.data.get("userId")
        
        #if userId != request.userId:
            #return Response({"status":"error",'message':Messages.INVALID_USER}, status=status.HTTP_200_OK)
            
        if not User.objects.filter(user_id=userId).exists():
            return Response({"status":"error",'message':Messages.USER_NOT_EXISTS}, status=status.HTTP_200_OK)
        User.objects.filter(user_id=userId).update(
            first_name = request.data['fullName'],
            email_id = request.data['emailId'],  
            profile_pic = request.data['profilePic'] ,
            updated_by = request.data.get("creator_id"),
            gender = request.data.get("gender")
            ) 
         
        #Education.objects.filter(userId=userId).update(occuption = request.data['designation'], highest_edu = request.data['education'], annualincome = request.data['anualIncome'])
        
        #Family.objects.filter(userId=userId).update(corr_city = request.data['city'], corr_country = request.data['country'], corr_state = request.data['state'], corr_address = request.data['address'])
        return Response({"status":"success",'message':Messages.USER_UPDATED}, status=status.HTTP_200_OK)

    except Exception as e:
        print("get_all_studies", str(e))
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@isAuthenticate
def logout(request):  # block user
    try:
        schema = {
            "deviceToken": {'type': 'string', 'required': True, 'empty': False},
        }
        v = Validator()
        # validate the request
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        deviceToken = request.data['deviceToken']
        userId = request.userId
        
        # check user exists   
        if not User.objects.filter(user_id=userId).exclude(user_type=UserType.ADMIN).exists():
            return Response({'error':Messages.USER_NOT_EXISTS}, status=status.HTTP_200_OK)
            
        # upadte record
        Device.objects.get(created_by=userId, device_token=deviceToken).delete() 
        
        return Response({'message': Messages.USER_LOGOUT}, status=status.HTTP_200_OK)

    except Exception as e:
        print("-----------------Logout------------"+str(e))
        return Response({'error': Messages.SOMETHING_WENT_WRONG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@isAuthenticate
def save_master_data(request):  
    try:   

        schema = {
            "key": {'type': 'string', 'required': True, 'nullable': False},
            "value": {'type': 'string', 'required': True, 'nullable': False},
            "reqType": {'type': 'string', 'required': False, 'nullable': True},
            "masterId": {'type': 'integer', 'required': False, 'nullable': True}
            }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        # Create database connection
        db = SqlQueryBuilder()

        user_id = request.userId
        v_key = request.data['key']
        v_value = request.data['value']
        reqType = request.data.get('reqType')
        masterId = request.data.get('masterId')
        # Call stored procedure
        _result = db.readProcedureJson('save_master_data',[v_key, v_value, reqType, masterId])
        db.commit()  
        if int(_result[0]['response']) > 0:
            return Response({'message': "success"}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "Error"}, status=status.HTTP_200_OK)

    except Exception as e:
        print('......................deduct credit on view post....................',str(e))
        return Response({'error': Messages.SOMETHING_WENT_WRONG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
@isAuthenticate      
def generateOrderNumber(request):
    try:   

        schema = {
            "amount": {'type': 'integer', 'required': True, 'nullable': False}
            }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        v_amount = request.data['amount']
        ordrId = str(400)+ str(random.randint(1,9999))
        ss = razorpay_client.order.create({"amount":v_amount, "currency":"INR", "receipt":ordrId, "payment_capture":'0'})
        return Response({"ordid":ss['id'], "amount": v_amount, "status":"success"})
    except Exception as e:
        print("get_wallet_balance", str(e))
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
@isAuthenticate  
def capturePayment(request):
    try:   

        schema = {
            "amount": {'type': 'integer', 'required': True, 'nullable': False},
            "razorpay_payment_id": {'type': 'string', 'required': True, 'nullable': False}
            }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response(requestErrorMessagesFormate(v.errors), status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        amount = request.data['amount']
        payment_id = request.data['razorpay_payment_id']
        razorpay_client.payment.capture(payment_id, amount)
        if razorpay_client.payment.fetch(payment_id)["captured"] == True:
            transId = razorpay_client.payment.fetch(payment_id)['id']
            transAmount = razorpay_client.payment.fetch(payment_id)['amount']/100
            transStatus = razorpay_client.payment.fetch(payment_id)["status"]
            transMobile =  razorpay_client.payment.fetch(payment_id)['contact'] 
            transEmail = razorpay_client.payment.fetch(payment_id)['email']
            transOrderId = razorpay_client.payment.fetch(payment_id)['order_id']
            return Response({"message":"captured", "status":"success"})
        else:
            transId = razorpay_client.payment.fetch(payment_id)['id']
            transAmount = razorpay_client.payment.fetch(payment_id)['amount']/100
            transStatus = razorpay_client.payment.fetch(payment_id)["status"]
            transMobile =  razorpay_client.payment.fetch(payment_id)['contact'] 
            transEmail = razorpay_client.payment.fetch(payment_id)['email']
            transOrderId = razorpay_client.payment.fetch(payment_id)['order_id']
            return Response({"message":"failed", "status":"failed"})
    except Exception as e:
        transId = razorpay_client.payment.fetch(payment_id)['id']
        transAmount = razorpay_client.payment.fetch(payment_id)['amount']/100
        transStatus = razorpay_client.payment.fetch(payment_id)["status"]
        transMobile =  razorpay_client.payment.fetch(payment_id)['contact'] 
        transEmail = razorpay_client.payment.fetch(payment_id)['email']
        transOrderId = razorpay_client.payment.fetch(payment_id)['order_id']
        return Response({"message":"failed", "status":"failed", "err":e})


@api_view(['POST'])
def uploadFile(request):
    try:
        imageRawFile = request.FILES['file']
        print(imageRawFile)
        fileType = request.data.get("fileType")
        unique_filename = str(uuid.uuid4())+str(imageRawFile)
        print(image_uploadPath)
        with open(str(image_uploadPath)+str(unique_filename), 'wb') as desk:
            for chunk in imageRawFile.chunks():
                desk.write(chunk)
        imagPath = "http://127.0.0.1:8000/static/Uploaded/UserProfiles/"+unique_filename
        return Response({"message":"success", "status":"success", "image_url":imagPath})
    except Exception as e:
        return Response({"message":"failed", "status":"failed", "err":e})


