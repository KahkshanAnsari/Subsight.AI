-- =============================================================================
-- SubSight AI — Supabase Database Schema
-- Version: 2.0 (Auth + Persistent Storage)
--
-- Run this entire script in the Supabase SQL Editor:
--   Dashboard → SQL Editor → New query → Paste → Run
--
-- What this creates:
--   1. subscriptions table (with user_id FK to auth.users)
--   2. Indexes for common query patterns
--   3. Row Level Security (RLS) — users only access their own rows
--   4. RLS policies for SELECT / INSERT / UPDATE / DELETE
--   5. Auto-update trigger for updated_at
-- =============================================================================


-- ---------------------------------------------------------------------------
-- 1. Extensions
-- ---------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


-- ---------------------------------------------------------------------------
-- 2. Subscriptions Table
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS subscriptions (
    -- Primary key: uses the app's existing sub_xxxxxxxx format (TEXT)
    id              TEXT            PRIMARY KEY,

    -- Foreign key to Supabase Auth — enforces ownership and cascades on user deletion
    user_id         UUID            NOT NULL
                    REFERENCES auth.users(id)
                    ON DELETE CASCADE,

    -- Core subscription fields (mirror the app's internal dict schema)
    name            TEXT            NOT NULL DEFAULT 'Unnamed Service',
    price           NUMERIC(12, 2)  NOT NULL DEFAULT 0.00,
    billing_cycle   TEXT            NOT NULL DEFAULT 'Monthly'
                    CHECK (billing_cycle IN ('Monthly', 'Quarterly', 'Yearly')),
    category        TEXT            NOT NULL DEFAULT 'Other'
                    CHECK (category IN (
                        'Entertainment',
                        'Productivity',
                        'Education',
                        'Cloud & Storage',
                        'Health & Fitness',
                        'Shopping',
                        'Other'
                    )),
    currency        TEXT            NOT NULL DEFAULT 'INR (₹)',
    renewal_date    DATE,
    status          TEXT            NOT NULL DEFAULT 'Active'
                    CHECK (status IN ('Active', 'Review Needed', 'Paused', 'Cancelled')),

    -- Audit timestamps
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);


-- ---------------------------------------------------------------------------
-- 3. Indexes
-- ---------------------------------------------------------------------------

-- Primary access pattern: all subscriptions for a given user
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id
    ON subscriptions (user_id);

-- Upcoming renewals query (30-day window)
CREATE INDEX IF NOT EXISTS idx_subscriptions_renewal_date
    ON subscriptions (renewal_date);

-- Status filtering (Active / Review Needed / Paused / Cancelled)
CREATE INDEX IF NOT EXISTS idx_subscriptions_status
    ON subscriptions (status);

-- Composite index for the most common query: user + status
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_status
    ON subscriptions (user_id, status);


-- ---------------------------------------------------------------------------
-- 4. Row Level Security
-- ---------------------------------------------------------------------------

-- Enable RLS on the table
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- IMPORTANT: Drop existing policies before recreating to allow safe re-runs
DROP POLICY IF EXISTS "Users can view own subscriptions"   ON subscriptions;
DROP POLICY IF EXISTS "Users can insert own subscriptions" ON subscriptions;
DROP POLICY IF EXISTS "Users can update own subscriptions" ON subscriptions;
DROP POLICY IF EXISTS "Users can delete own subscriptions" ON subscriptions;


-- ---------------------------------------------------------------------------
-- 5. RLS Policies
-- ---------------------------------------------------------------------------

-- SELECT: a user may only read their own rows
CREATE POLICY "Users can view own subscriptions"
    ON subscriptions
    FOR SELECT
    USING (auth.uid() = user_id);

-- INSERT: a user may only insert rows where user_id matches their own UID
CREATE POLICY "Users can insert own subscriptions"
    ON subscriptions
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- UPDATE: a user may only update their own rows
CREATE POLICY "Users can update own subscriptions"
    ON subscriptions
    FOR UPDATE
    USING     (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- DELETE: a user may only delete their own rows
CREATE POLICY "Users can delete own subscriptions"
    ON subscriptions
    FOR DELETE
    USING (auth.uid() = user_id);


-- ---------------------------------------------------------------------------
-- 6. Auto-update trigger for updated_at
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop existing trigger if re-running this script
DROP TRIGGER IF EXISTS trigger_subscriptions_updated_at ON subscriptions;

CREATE TRIGGER trigger_subscriptions_updated_at
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- ---------------------------------------------------------------------------
-- Verification queries (optional — uncomment to test after running)
-- ---------------------------------------------------------------------------
-- SELECT table_name FROM information_schema.tables WHERE table_name = 'subscriptions';
-- SELECT policyname, cmd FROM pg_policies WHERE tablename = 'subscriptions';
-- SELECT indexname FROM pg_indexes WHERE tablename = 'subscriptions';
