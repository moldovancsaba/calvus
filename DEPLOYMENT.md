
# Deployment Guide

## Prerequisites

### Required Accounts
- [ ] Supabase account (free tier sufficient for development)
- [ ] MongoDB Atlas account (free tier sufficient for development)
- [ ] GitHub account (for version control)

### Environment Setup
- [ ] Node.js 18+ installed
- [ ] npm or yarn package manager
- [ ] Git configured with your credentials

## Step-by-Step Deployment

### 1. MongoDB Atlas Configuration

1. **Create MongoDB Cluster**
   - Sign up at [MongoDB Atlas](https://cloud.mongodb.com/)
   - Create new cluster (M0 free tier works fine)
   - Choose cloud provider and region closest to your users

2. **Database Access Setup**
   - Go to Database Access → Add New Database User
   - Choose "Password" authentication
   - Create username/password (save these for connection string)
   - Grant "Atlas admin" role for simplicity

3. **Network Access Configuration**
   - Go to Network Access → Add IP Address
   - Choose "Allow access from anywhere" (0.0.0.0/0) for development
   - For production, restrict to specific IPs/CIDR blocks

4. **Get Connection String**
   - Go to Databases → Connect → Connect your application
   - Copy the connection string
   - Replace `<password>` with your database user password
   - Format: `mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority&appName=YourApp`

### 2. Supabase Project Setup

1. **Create Supabase Project**
   - Sign up at [Supabase](https://supabase.com/)
   - Create new project
   - Choose organization and project name
   - Select region and database password

2. **Configure MongoDB Secret**
   - Go to Project Settings → Edge Functions
   - Add new secret: `MONGODB_URI`
   - Paste your MongoDB connection string as the value
   - Save the secret

### 3. Local Development Setup

1. **Clone Repository**
   ```bash
   git clone <your-repository-url>
   cd triangle-mesh-map
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Configure Supabase**
   - Update `src/integrations/supabase/client.ts` with your project URL and anon key
   - These are found in Project Settings → API

4. **Start Development Server**
   ```bash
   npm run dev
   ```

### 4. Production Deployment

#### Option A: Deploy via Lovable (Recommended)
1. **Push to Lovable**
   - Use Lovable's built-in deployment
   - Click "Publish" in the Lovable interface
   - Custom domain can be configured in Project Settings

#### Option B: Deploy to Vercel
1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel --prod
   ```

3. **Configure Environment**
   - Add `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` in Vercel dashboard
   - MongoDB URI is already configured in Supabase secrets

#### Option C: Deploy to Netlify
1. **Build Project**
   ```bash
   npm run build
   ```

2. **Deploy**
   - Upload `dist` folder to Netlify
   - Or connect GitHub repository for automatic deployments

## Configuration Checklist

### MongoDB Atlas
- [ ] Cluster created and running
- [ ] Database user created with appropriate permissions
- [ ] Network access configured (0.0.0.0/0 for dev, restricted for prod)
- [ ] Connection string copied and tested

### Supabase
- [ ] Project created
- [ ] `MONGODB_URI` secret configured in Edge Functions settings
- [ ] Edge function `triangle-activity` deployed automatically
- [ ] Project URL and anon key noted for client configuration

### Application
- [ ] Dependencies installed (`npm install`)
- [ ] Supabase client configured with correct URL/key
- [ ] Application starts without errors (`npm run dev`)
- [ ] Triangle interactions work (check browser console for logs)
- [ ] MongoDB storage confirmed (check edge function logs)

## Testing Your Deployment

### 1. Functionality Test
1. **Open Application**
   - Navigate to your deployed URL
   - Verify map loads with three base triangles

2. **Test Triangle Interaction**
   - Click on a triangle multiple times
   - Verify color changes with each click (10% gray increments)
   - Confirm 11th click triggers subdivision

3. **Test Persistence**
   - Make several triangle clicks
   - Refresh the page
   - Verify previous clicks are restored from MongoDB

4. **Test Real-time Sync**
   - Open application in two browser tabs
   - Click triangles in one tab
   - Verify changes appear in other tab within 5 seconds

### 2. Performance Test
- [ ] Map loads within 3 seconds
- [ ] Triangle clicks respond immediately
- [ ] Real-time updates work smoothly
- [ ] No console errors during normal operation

### 3. Error Scenarios
- [ ] Application handles MongoDB connection failures gracefully
- [ ] Network interruptions don't crash the application
- [ ] Invalid triangle operations are handled safely

## Monitoring & Maintenance

### Logs and Debugging
1. **Supabase Edge Function Logs**
   - Go to Supabase Dashboard → Edge Functions → triangle-activity → Logs
   - Monitor for MongoDB connection issues
   - Check for API errors and performance metrics

2. **MongoDB Atlas Monitoring**
   - Go to Atlas Dashboard → Monitoring
   - Track connection counts and query performance
   - Set up alerts for unusual activity

3. **Browser Console**
   - Check for JavaScript errors
   - Monitor triangle activity logs
   - Verify API call success/failure

### Regular Maintenance
- [ ] Monitor MongoDB storage usage (free tier has 512MB limit)
- [ ] Check Supabase function invocation limits
- [ ] Review application performance metrics
- [ ] Update dependencies regularly (`npm audit` and `npm update`)

### Scaling Considerations
- **MongoDB**: Upgrade to paid tier when approaching 512MB limit
- **Supabase**: Monitor edge function invocations (500K/month on free tier)
- **Traffic**: Consider CDN for high-traffic deployments

## Troubleshooting Common Issues

### MongoDB Connection Errors
```
Error: Failed to store activity: MongoServerError
```
**Solutions:**
- Verify MongoDB URI is correct in Supabase secrets
- Check MongoDB Atlas network access settings
- Ensure database user has proper permissions

### Triangle Not Loading
```
No triangles visible on map load
```
**Solutions:**
- Check browser console for JavaScript errors
- Verify Supabase client configuration
- Test edge function directly in Supabase dashboard

### Real-time Updates Not Working
```
Changes don't appear in other browser tabs
```
**Solutions:**
- Check edge function logs for polling errors
- Verify MongoDB connection stability
- Test with longer polling intervals (increase from 5 seconds)

## Security for Production

### MongoDB Security
- [ ] Restrict network access to specific IP ranges
- [ ] Use database-specific user (not Atlas admin)
- [ ] Enable MongoDB access logs
- [ ] Regular security updates

### Supabase Security
- [ ] Review RLS policies (if implementing user accounts)
- [ ] Monitor edge function usage for abuse
- [ ] Configure appropriate CORS settings
- [ ] Regular project security review

### Application Security
- [ ] Implement rate limiting for triangle clicks
- [ ] Validate all user inputs
- [ ] Monitor for suspicious activity patterns
- [ ] Regular dependency security audits

---

Your Triangle Mesh application is now ready for production deployment! 🎉
