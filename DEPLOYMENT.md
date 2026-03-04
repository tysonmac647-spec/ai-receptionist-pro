# AI Receptionist Pro - Deployment Guide

## Overview
Complete guide to deploy and test your AI Receptionist System

## Prerequisites
- GitHub account (✓ Created)
- Railway account (✓ Created)
- Twilio account (✓ Created)
- OpenAI account (✓ Created)
- Stripe account (✓ Created)
- Landing page: ai-receptionist-pro.carrd.co (✓ Created)

## Step 1: Deploy to Railway

1. Go to https://railway.com
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account
5. Select: tysonmac647-spec/ai-receptionist-pro
6. Railway will automatically detect the Procfile

## Step 2: Configure Environment Variables in Railway

Add these in Railway Settings > Variables:

```
OPENAI_API_KEY=<your-openai-key>
TWILIO_ACCOUNT_SID=<your-twilio-sid>
TWILIO_AUTH_TOKEN=<your-twilio-token>
TWILIO_PHONE_NUMBER=<your-twilio-number>
STRIPE_API_KEY=<your-stripe-secret-key>
STRIPE_WEBHOOK_SECRET=<your-webhook-secret>
BUSINESS_NAME=AI Receptionist Pro
BUSINESS_HOURS=Monday-Friday 9AM-5PM
BUSINESS_EMAIL=contact@ai-receptionist-pro.carrd.co
```

## Step 3: Get Your Deployment URL

After deployment, Railway provides a public URL:
- Format: https://your-app.railway.app
- Copy this URL for Twilio configuration

## Step 4: Configure Twilio Webhook

1. Go to Twilio Console > Phone Numbers
2. Select your AI Receptionist phone number
3. Under "Voice & Fax", set:
   - A CALL COMES IN: Webhook
   - URL: https://your-app.railway.app/voice
   - HTTP Method: POST
4. Save configuration

## Step 5: Configure Stripe Webhooks

1. Go to Stripe Dashboard > Developers > Webhooks
2. Click "Add endpoint"
3. Endpoint URL: https://your-app.railway.app/webhook/stripe
4. Select events:
   - customer.subscription.created
   - customer.subscription.updated
   - customer.subscription.deleted
   - invoice.payment_succeeded
   - invoice.payment_failed
5. Copy the webhook signing secret
6. Update STRIPE_WEBHOOK_SECRET in Railway

## Step 6: Test Your AI Receptionist

### Test 1: Health Check
```bash
curl https://your-app.railway.app/health
```
Expected: {"status": "healthy"}

### Test 2: Make a Test Call
1. Call your Twilio phone number
2. The AI should answer and greet you
3. Try asking:
   - "What are your business hours?"
   - "I'd like to book an appointment"
   - "Can you help me?"

### Test 3: Subscription Flow
1. Visit: https://your-app.railway.app/subscribe
2. Complete payment form
3. Verify subscription in Stripe Dashboard

## Monitoring

### Railway Logs
- Go to Railway Dashboard
- Select your project
- Click "Deployments" > "View Logs"
- Monitor real-time activity

### Twilio Logs
- Twilio Console > Monitor > Logs > Calls
- Check call recordings and transcripts

### Stripe Dashboard
- Monitor subscriptions
- Track payments
- View customer data

## Pricing Configuration

Update in Stripe Dashboard:
1. Products > Add Product
2. Name: "AI Receptionist Pro"
3. Price: £299/month
4. Copy the Price ID
5. Update in app.py STRIPE_PRICE_ID

## Troubleshooting

### Issue: Deployment Failed
- Check Railway logs for errors
- Verify all environment variables are set
- Ensure requirements.txt is correct

### Issue: AI Not Responding
- Verify OpenAI API key is valid
- Check Railway logs for API errors
- Test API key independently

### Issue: Calls Not Working
- Verify Twilio webhook URL is correct
- Check Twilio phone number configuration
- Review Twilio error logs

### Issue: Payments Failing
- Verify Stripe API keys (use test keys first)
- Check webhook configuration
- Review Stripe Dashboard logs

## Production Checklist

- [ ] All environment variables configured
- [ ] Twilio webhook connected
- [ ] Stripe webhooks configured  
- [ ] Test call completed successfully
- [ ] Test subscription payment works
- [ ] Landing page updated with correct pricing
- [ ] Monitoring setup complete
- [ ] Switch Stripe to live mode
- [ ] Update landing page with live payment link

## Next Steps

1. Test thoroughly with test phone numbers
2. Create marketing materials
3. Set up customer support
4. Launch marketing campaign
5. Monitor performance and customer feedback

## Support

For issues:
- Railway: https://railway.app/help
- Twilio: https://www.twilio.com/help
- OpenAI: https://help.openai.com
- Stripe: https://support.stripe.com
